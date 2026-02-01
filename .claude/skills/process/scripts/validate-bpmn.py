#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BPMN Validation Script for Periscope Platform

Validates BPMN files locally before upload, catching errors early
and saving API round-trips.

Validation Levels:
  1. XML Well-formedness - Basic XML parsing
  2. BPMN Schema - Validates against BPMN 2.0 XSD (optional)
  3. Structural - Required elements, unique IDs
  4. Flow Connectivity - All elements connected, no orphans
  5. Periscope Rules - AI agents, functions, user tasks configured

Usage:
  python validate-bpmn.py <file.bpmn> [--strict] [--json]

Options:
  --strict    Fail on warnings (default: warnings don't fail)
  --json      Output results as JSON
  --verbose   Show detailed validation info
  --no-color  Disable colored output
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET

# BPMN Namespaces
NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
    "periscope": "http://periscope.dev/schema/bpmn",
}


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    level: int
    severity: Severity
    code: str
    message: str
    element_id: Optional[str] = None
    element_type: Optional[str] = None
    suggestion: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "severity": self.severity.value,
            "code": self.code,
            "message": self.message,
            "element_id": self.element_id,
            "element_type": self.element_type,
            "suggestion": self.suggestion,
        }


@dataclass
class ValidationResult:
    file_path: str
    valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    element_counts: dict = field(default_factory=dict)

    def add_issue(self, issue: ValidationIssue):
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.valid = False

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == Severity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == Severity.WARNING]

    def to_dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "valid": self.valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "element_counts": self.element_counts,
            "issues": [i.to_dict() for i in self.issues],
        }


class BPMNValidator:
    """Multi-level BPMN validator for Periscope platform."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.result = ValidationResult(file_path=file_path)
        self.tree: Optional[ET.ElementTree] = None
        self.root: Optional[ET.Element] = None
        self.elements: dict[str, ET.Element] = {}
        self.sequence_flows: list[tuple[str, str]] = []

    def validate(self) -> ValidationResult:
        """Run all validation levels."""
        # Level 1: XML Well-formedness
        if not self._validate_xml():
            return self.result

        # Level 2: BPMN Schema (informational - XSD validation is optional)
        self._validate_bpmn_basics()

        # Level 3: Structural validation
        self._validate_structure()

        # Level 4: Flow connectivity
        self._validate_connectivity()

        # Level 5: Periscope-specific rules
        self._validate_periscope_rules()

        return self.result

    # =========================================================================
    # Level 1: XML Well-formedness
    # =========================================================================

    def _validate_xml(self) -> bool:
        """Validate XML is well-formed."""
        try:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            return True
        except ET.ParseError as e:
            self.result.add_issue(ValidationIssue(
                level=1,
                severity=Severity.ERROR,
                code="XML_PARSE_ERROR",
                message=f"XML parsing failed: {e}",
                suggestion="Check for unclosed tags, invalid characters, or encoding issues"
            ))
            return False
        except FileNotFoundError:
            self.result.add_issue(ValidationIssue(
                level=1,
                severity=Severity.ERROR,
                code="FILE_NOT_FOUND",
                message=f"File not found: {self.file_path}"
            ))
            return False

    # =========================================================================
    # Level 2: BPMN Basics
    # =========================================================================

    def _validate_bpmn_basics(self):
        """Validate basic BPMN structure."""
        # Check root element
        root_tag = self.root.tag
        if not root_tag.endswith("definitions"):
            self.result.add_issue(ValidationIssue(
                level=2,
                severity=Severity.ERROR,
                code="INVALID_ROOT",
                message=f"Root element must be 'definitions', found: {root_tag}",
                suggestion="Wrap content in <bpmn:definitions> element"
            ))
            return

        # Check namespaces
        if "http://www.omg.org/spec/BPMN/20100524/MODEL" not in str(self.root.attrib):
            # Check if it's in the tag itself
            if "{http://www.omg.org/spec/BPMN/20100524/MODEL}" not in root_tag:
                self.result.add_issue(ValidationIssue(
                    level=2,
                    severity=Severity.WARNING,
                    code="MISSING_BPMN_NAMESPACE",
                    message="BPMN namespace not found in root element",
                    suggestion="Add xmlns:bpmn=\"http://www.omg.org/spec/BPMN/20100524/MODEL\""
                ))

        # Find process element
        process = self.root.find(".//bpmn:process", NS)
        if process is None:
            process = self.root.find(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}process")
        if process is None:
            self.result.add_issue(ValidationIssue(
                level=2,
                severity=Severity.ERROR,
                code="NO_PROCESS",
                message="No <process> element found",
                suggestion="Add a <bpmn:process> element inside definitions"
            ))
            return

        # Check process has ID
        process_id = process.get("id")
        if not process_id:
            self.result.add_issue(ValidationIssue(
                level=2,
                severity=Severity.ERROR,
                code="PROCESS_NO_ID",
                message="Process element missing 'id' attribute",
                suggestion="Add id attribute to process element"
            ))

    # =========================================================================
    # Level 3: Structural Validation
    # =========================================================================

    def _validate_structure(self):
        """Validate BPMN structure: required elements, unique IDs."""
        # Build element index
        self._index_elements()

        # Count elements
        self._count_elements()

        # Check for start event
        start_events = [e for e in self.elements.values()
                       if self._local_name(e.tag) == "startEvent"]
        if not start_events:
            self.result.add_issue(ValidationIssue(
                level=3,
                severity=Severity.ERROR,
                code="NO_START_EVENT",
                message="No start event found",
                suggestion="Add a <bpmn:startEvent> element"
            ))

        # Check for end event
        end_events = [e for e in self.elements.values()
                     if self._local_name(e.tag) == "endEvent"]
        if not end_events:
            self.result.add_issue(ValidationIssue(
                level=3,
                severity=Severity.ERROR,
                code="NO_END_EVENT",
                message="No end event found",
                suggestion="Add a <bpmn:endEvent> element"
            ))

        # Check for duplicate IDs
        self._check_duplicate_ids()

        # Check ID format
        self._check_id_format()

    def _index_elements(self):
        """Build index of all BPMN elements by ID."""
        for elem in self.root.iter():
            elem_id = elem.get("id")
            if elem_id:
                self.elements[elem_id] = elem

            # Track sequence flows
            local_name = self._local_name(elem.tag)
            if local_name == "sequenceFlow":
                source = elem.get("sourceRef")
                target = elem.get("targetRef")
                if source and target:
                    self.sequence_flows.append((source, target))

    def _count_elements(self):
        """Count different element types."""
        counts = defaultdict(int)
        for elem in self.elements.values():
            local_name = self._local_name(elem.tag)
            counts[local_name] += 1
        self.result.element_counts = dict(counts)

    def _check_duplicate_ids(self):
        """Check for duplicate IDs."""
        seen_ids = {}
        for elem in self.root.iter():
            elem_id = elem.get("id")
            if elem_id:
                if elem_id in seen_ids:
                    self.result.add_issue(ValidationIssue(
                        level=3,
                        severity=Severity.ERROR,
                        code="DUPLICATE_ID",
                        message=f"Duplicate ID: '{elem_id}'",
                        element_id=elem_id,
                        suggestion="Ensure all elements have unique IDs"
                    ))
                seen_ids[elem_id] = elem

    def _check_id_format(self):
        """Check ID format (no spaces, special characters)."""
        invalid_pattern = re.compile(r"[^a-zA-Z0-9_-]")
        for elem_id in self.elements:
            if invalid_pattern.search(elem_id):
                self.result.add_issue(ValidationIssue(
                    level=3,
                    severity=Severity.WARNING,
                    code="INVALID_ID_FORMAT",
                    message=f"ID contains invalid characters: '{elem_id}'",
                    element_id=elem_id,
                    suggestion="Use only alphanumeric characters, hyphens, and underscores"
                ))

    # =========================================================================
    # Level 4: Flow Connectivity
    # =========================================================================

    def _validate_connectivity(self):
        """Validate flow connectivity: all elements connected, no orphans."""
        # Build adjacency lists
        outgoing = defaultdict(set)
        incoming = defaultdict(set)

        for source, target in self.sequence_flows:
            outgoing[source].add(target)
            incoming[target].add(source)

        # Check for invalid references
        for source, target in self.sequence_flows:
            if source not in self.elements:
                self.result.add_issue(ValidationIssue(
                    level=4,
                    severity=Severity.ERROR,
                    code="INVALID_SOURCE_REF",
                    message=f"Sequence flow references non-existent source: '{source}'",
                    suggestion="Check sourceRef attribute on sequence flows"
                ))
            if target not in self.elements:
                self.result.add_issue(ValidationIssue(
                    level=4,
                    severity=Severity.ERROR,
                    code="INVALID_TARGET_REF",
                    message=f"Sequence flow references non-existent target: '{target}'",
                    suggestion="Check targetRef attribute on sequence flows"
                ))

        # Check for orphan nodes (excluding start/end events and data objects)
        flow_elements = {"task", "serviceTask", "userTask", "scriptTask", "sendTask",
                        "receiveTask", "manualTask", "businessRuleTask", "callActivity",
                        "subProcess", "exclusiveGateway", "parallelGateway",
                        "inclusiveGateway", "eventBasedGateway", "complexGateway",
                        "intermediateCatchEvent", "intermediateThrowEvent"}

        for elem_id, elem in self.elements.items():
            local_name = self._local_name(elem.tag)

            if local_name in flow_elements:
                has_incoming = elem_id in incoming or len(incoming[elem_id]) > 0
                has_outgoing = elem_id in outgoing or len(outgoing[elem_id]) > 0

                if not has_incoming and not has_outgoing:
                    self.result.add_issue(ValidationIssue(
                        level=4,
                        severity=Severity.ERROR,
                        code="ORPHAN_ELEMENT",
                        message=f"Element has no connections: '{elem_id}'",
                        element_id=elem_id,
                        element_type=local_name,
                        suggestion="Connect this element with sequence flows"
                    ))

        # Check gateways have proper connections
        self._validate_gateways(outgoing, incoming)

    def _validate_gateways(self, outgoing: dict, incoming: dict):
        """Validate gateway configurations."""
        gateway_types = {"exclusiveGateway", "parallelGateway", "inclusiveGateway"}

        for elem_id, elem in self.elements.items():
            local_name = self._local_name(elem.tag)

            if local_name in gateway_types:
                out_count = len(outgoing.get(elem_id, []))
                in_count = len(incoming.get(elem_id, []))

                # Split gateway should have multiple outgoing
                if in_count == 1 and out_count < 2:
                    self.result.add_issue(ValidationIssue(
                        level=4,
                        severity=Severity.WARNING,
                        code="GATEWAY_SINGLE_OUTPUT",
                        message=f"Gateway has only one outgoing flow: '{elem_id}'",
                        element_id=elem_id,
                        element_type=local_name,
                        suggestion="Gateways typically need multiple outgoing paths"
                    ))

                # Check exclusive gateway has conditions
                if local_name == "exclusiveGateway" and out_count > 1:
                    self._check_gateway_conditions(elem_id, outgoing[elem_id])

    def _check_gateway_conditions(self, gateway_id: str, targets: set):
        """Check that exclusive gateway outgoing flows have conditions."""
        has_default = False
        missing_conditions = []

        for elem_id, elem in self.elements.items():
            local_name = self._local_name(elem.tag)
            if local_name == "sequenceFlow":
                source = elem.get("sourceRef")
                if source == gateway_id:
                    # Check for condition
                    condition = elem.find("bpmn:conditionExpression", NS) or \
                               elem.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}conditionExpression")
                    is_default = elem.get("isDefault") == "true" or \
                                elem.get("{http://www.omg.org/spec/BPMN/20100524/MODEL}isDefault") == "true"

                    if is_default:
                        has_default = True
                    elif condition is None:
                        missing_conditions.append(elem_id)

        # All non-default flows should have conditions
        if missing_conditions and not (len(missing_conditions) == 1 and not has_default):
            for flow_id in missing_conditions:
                self.result.add_issue(ValidationIssue(
                    level=4,
                    severity=Severity.WARNING,
                    code="MISSING_CONDITION",
                    message=f"Exclusive gateway flow missing condition: '{flow_id}'",
                    element_id=flow_id,
                    suggestion="Add conditionExpression or mark as default flow"
                ))

    # =========================================================================
    # Level 5: Periscope-Specific Rules
    # =========================================================================

    def _validate_periscope_rules(self):
        """Validate Periscope-specific configurations."""
        for elem_id, elem in self.elements.items():
            local_name = self._local_name(elem.tag)

            if local_name == "serviceTask":
                self._validate_service_task(elem_id, elem)
            elif local_name == "userTask":
                self._validate_user_task(elem_id, elem)
            elif local_name == "scriptTask":
                self._validate_script_task(elem_id, elem)
            elif local_name == "sendTask":
                self._validate_send_task(elem_id, elem)
            elif local_name == "callActivity":
                self._validate_call_activity(elem_id, elem)
            elif "timerEvent" in local_name or local_name in ["intermediateCatchEvent", "boundaryEvent"]:
                self._validate_timer_event(elem_id, elem)

    def _validate_service_task(self, elem_id: str, elem: ET.Element):
        """Validate service task has AI agent configuration."""
        extensions = elem.find("bpmn:extensionElements", NS) or \
                    elem.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}extensionElements")

        if extensions is None:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.ERROR,
                code="SERVICE_TASK_NO_CONFIG",
                message=f"Service task missing configuration: '{elem_id}'",
                element_id=elem_id,
                element_type="serviceTask",
                suggestion="Add periscope:AIAgentConfiguration in extensionElements"
            ))
            return

        # Look for AI agent configuration
        agent_config = extensions.find("periscope:AIAgentConfiguration", NS) or \
                      extensions.find("{http://periscope.dev/schema/bpmn}AIAgentConfiguration")

        if agent_config is None:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.ERROR,
                code="SERVICE_TASK_NO_AGENT",
                message=f"Service task missing AI agent configuration: '{elem_id}'",
                element_id=elem_id,
                element_type="serviceTask",
                suggestion="Add periscope:AIAgentConfiguration element"
            ))
            return

        # Validate agent configuration
        agent_id = agent_config.get("agentId")
        agent_type = agent_config.get("agentType")

        if not agent_id and not agent_type:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.ERROR,
                code="AGENT_CONFIG_INCOMPLETE",
                message=f"Agent configuration missing agentId or agentType: '{elem_id}'",
                element_id=elem_id,
                element_type="serviceTask",
                suggestion="Specify either agentId (existing agent) or agentType (inline config)"
            ))

        # Check for inline agent without prompt
        if agent_type and not agent_id:
            prompt = agent_config.get("prompt")
            if not prompt:
                self.result.add_issue(ValidationIssue(
                    level=5,
                    severity=Severity.WARNING,
                    code="AGENT_NO_PROMPT",
                    message=f"Inline agent missing prompt: '{elem_id}'",
                    element_id=elem_id,
                    element_type="serviceTask",
                    suggestion="Add prompt attribute for inline agent configuration"
                ))

    def _validate_user_task(self, elem_id: str, elem: ET.Element):
        """Validate user task has assignee or candidate groups."""
        extensions = elem.find("bpmn:extensionElements", NS) or \
                    elem.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}extensionElements")

        task_def = None
        if extensions:
            task_def = extensions.find("periscope:TaskDefinition", NS) or \
                      extensions.find("{http://periscope.dev/schema/bpmn}TaskDefinition")

        # Check for assignee in task definition or standard BPMN attributes
        assignee = elem.get("assignee") or elem.get("{http://periscope.dev/schema/bpmn}assignee")
        candidate_groups = elem.get("candidateGroups") or elem.get("{http://periscope.dev/schema/bpmn}candidateGroups")

        if task_def:
            assignee = assignee or task_def.get("assignee")

        if not assignee and not candidate_groups:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.WARNING,
                code="USER_TASK_NO_ASSIGNEE",
                message=f"User task has no assignee or candidate groups: '{elem_id}'",
                element_id=elem_id,
                element_type="userTask",
                suggestion="Add assignee or candidateGroups attribute"
            ))

    def _validate_script_task(self, elem_id: str, elem: ET.Element):
        """Validate script task has function configuration."""
        extensions = elem.find("bpmn:extensionElements", NS) or \
                    elem.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}extensionElements")

        if extensions is None:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.ERROR,
                code="SCRIPT_TASK_NO_CONFIG",
                message=f"Script task missing configuration: '{elem_id}'",
                element_id=elem_id,
                element_type="scriptTask",
                suggestion="Add periscope:ScriptTaskConfiguration in extensionElements"
            ))
            return

        script_config = extensions.find("periscope:ScriptTaskConfiguration", NS) or \
                       extensions.find("{http://periscope.dev/schema/bpmn}ScriptTaskConfiguration")

        if script_config is None:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.ERROR,
                code="SCRIPT_TASK_NO_FUNCTION",
                message=f"Script task missing function configuration: '{elem_id}'",
                element_id=elem_id,
                element_type="scriptTask",
                suggestion="Add periscope:ScriptTaskConfiguration element"
            ))
            return

        function_id = script_config.get("functionId")
        function_name = script_config.get("functionName")

        if not function_id and not function_name:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.ERROR,
                code="FUNCTION_CONFIG_INCOMPLETE",
                message=f"Function configuration missing functionId or functionName: '{elem_id}'",
                element_id=elem_id,
                element_type="scriptTask",
                suggestion="Specify functionId or functionName"
            ))

    def _validate_send_task(self, elem_id: str, elem: ET.Element):
        """Validate send task has email configuration."""
        extensions = elem.find("bpmn:extensionElements", NS) or \
                    elem.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}extensionElements")

        if extensions is None:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.WARNING,
                code="SEND_TASK_NO_CONFIG",
                message=f"Send task missing email configuration: '{elem_id}'",
                element_id=elem_id,
                element_type="sendTask",
                suggestion="Add periscope:SendTaskConfiguration in extensionElements"
            ))
            return

        send_config = extensions.find("periscope:SendTaskConfiguration", NS) or \
                     extensions.find("{http://periscope.dev/schema/bpmn}SendTaskConfiguration")

        if send_config is None:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.WARNING,
                code="SEND_TASK_NO_EMAIL",
                message=f"Send task missing email configuration: '{elem_id}'",
                element_id=elem_id,
                element_type="sendTask",
                suggestion="Add periscope:SendTaskConfiguration element"
            ))

    def _validate_call_activity(self, elem_id: str, elem: ET.Element):
        """Validate call activity has child workflow configuration."""
        extensions = elem.find("bpmn:extensionElements", NS) or \
                    elem.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}extensionElements")

        # Check for calledElement attribute
        called_element = elem.get("calledElement")

        if not called_element:
            if extensions:
                call_config = extensions.find("periscope:CallActivityConfiguration", NS) or \
                             extensions.find("{http://periscope.dev/schema/bpmn}CallActivityConfiguration")
                if call_config:
                    called_element = call_config.get("calledElement")

        if not called_element:
            self.result.add_issue(ValidationIssue(
                level=5,
                severity=Severity.ERROR,
                code="CALL_ACTIVITY_NO_TARGET",
                message=f"Call activity missing calledElement: '{elem_id}'",
                element_id=elem_id,
                element_type="callActivity",
                suggestion="Specify calledElement attribute or CallActivityConfiguration"
            ))

    def _validate_timer_event(self, elem_id: str, elem: ET.Element):
        """Validate timer events have duration/date configuration."""
        timer_def = elem.find(".//bpmn:timerEventDefinition", NS) or \
                   elem.find(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}timerEventDefinition")

        if timer_def is not None:
            # Check for duration, date, or cycle
            duration = timer_def.find("bpmn:timeDuration", NS) or \
                      timer_def.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}timeDuration")
            date = timer_def.find("bpmn:timeDate", NS) or \
                  timer_def.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}timeDate")
            cycle = timer_def.find("bpmn:timeCycle", NS) or \
                   timer_def.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}timeCycle")

            if duration is None and date is None and cycle is None:
                self.result.add_issue(ValidationIssue(
                    level=5,
                    severity=Severity.ERROR,
                    code="TIMER_NO_DEFINITION",
                    message=f"Timer event missing duration/date/cycle: '{elem_id}'",
                    element_id=elem_id,
                    element_type=self._local_name(elem.tag),
                    suggestion="Add timeDuration, timeDate, or timeCycle element"
                ))

    # =========================================================================
    # Utility Methods
    # =========================================================================

    @staticmethod
    def _local_name(tag: str) -> str:
        """Extract local name from qualified tag."""
        if "}" in tag:
            return tag.split("}")[1]
        return tag


# =============================================================================
# CLI Output Formatting
# =============================================================================

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_result(result: ValidationResult, use_color: bool = True, verbose: bool = False):
    """Print validation result to console."""
    c = Colors if use_color else type("NoColor", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()

    print(f"\n{c.BOLD}BPMN Validation Report{c.RESET}")
    print(f"{'=' * 50}")
    print(f"File: {result.file_path}")
    print()

    # Element counts
    if result.element_counts and verbose:
        print(f"{c.CYAN}Element Counts:{c.RESET}")
        for elem_type, count in sorted(result.element_counts.items()):
            print(f"  {elem_type}: {count}")
        print()

    # Group issues by level
    issues_by_level: dict[int, list[ValidationIssue]] = defaultdict(list)
    for issue in result.issues:
        issues_by_level[issue.level].append(issue)

    level_names = {
        1: "XML Well-formedness",
        2: "BPMN Schema",
        3: "Structural Validation",
        4: "Flow Connectivity",
        5: "Periscope Rules",
    }

    for level in sorted(issues_by_level.keys()):
        issues = issues_by_level[level]
        errors = [i for i in issues if i.severity == Severity.ERROR]
        warnings = [i for i in issues if i.severity == Severity.WARNING]

        level_name = level_names.get(level, f"Level {level}")

        if errors:
            status = f"{c.RED}FAIL{c.RESET}"
        elif warnings:
            status = f"{c.YELLOW}WARN{c.RESET}"
        else:
            status = f"{c.GREEN}PASS{c.RESET}"

        print(f"Level {level}: {level_name} [{status}]")

        for issue in issues:
            if issue.severity == Severity.ERROR:
                icon = f"{c.RED}✗{c.RESET}"
            elif issue.severity == Severity.WARNING:
                icon = f"{c.YELLOW}⚠{c.RESET}"
            else:
                icon = f"{c.BLUE}ℹ{c.RESET}"

            elem_info = f" ({issue.element_id})" if issue.element_id else ""
            print(f"  {icon} [{issue.code}] {issue.message}{elem_info}")

            if verbose and issue.suggestion:
                print(f"      └─ {c.CYAN}Suggestion:{c.RESET} {issue.suggestion}")

        if not issues:
            print(f"  {c.GREEN}✓{c.RESET} All checks passed")
        print()

    # Summary
    print(f"{'=' * 50}")
    if result.valid:
        print(f"{c.GREEN}{c.BOLD}✓ VALID{c.RESET} - Ready for upload")
    else:
        print(f"{c.RED}{c.BOLD}✗ INVALID{c.RESET} - {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate BPMN files for Periscope platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Validation Levels:
  1. XML Well-formedness - Basic XML parsing
  2. BPMN Schema        - Root element, namespaces
  3. Structural         - Start/end events, unique IDs
  4. Connectivity       - Flow connections, gateway logic
  5. Periscope Rules    - AI agents, functions, user tasks

Examples:
  %(prog)s process.bpmn
  %(prog)s process.bpmn --strict --verbose
  %(prog)s process.bpmn --json > report.json
        """
    )
    parser.add_argument("file", help="BPMN file to validate")
    parser.add_argument("--strict", action="store_true",
                       help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed output with suggestions")
    parser.add_argument("--no-color", action="store_true",
                       help="Disable colored output")

    args = parser.parse_args()

    # Validate file exists
    if not Path(args.file).exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Run validation
    validator = BPMNValidator(args.file)
    result = validator.validate()

    # Apply strict mode
    if args.strict and result.warnings:
        result.valid = False

    # Output
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        use_color = not args.no_color and sys.stdout.isatty()
        print_result(result, use_color=use_color, verbose=args.verbose)

    # Exit code
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
