# Periscope BPMN Extensions Reference

This document describes the custom Periscope extensions for BPMN 2.0 process definitions.

## Namespace

All Periscope extensions use the following namespace:

```xml
xmlns:periscope="http://periscope.dev/schema/bpmn"
```

## Extension Elements Overview

| Element | Used In | Purpose |
|---------|---------|---------|
| `processVariables` | Process | Define workflow input/output variables |
| `aIAgentConfiguration` | Service Task | Configure AI agent execution |
| `taskDefinition` | User Task | Human task assignment and forms |
| `sendTaskConfiguration` | Send Task | Email sending configuration |
| `scriptTaskConfiguration` | Script Task | Sandboxed function execution |
| `emailTriggerConfiguration` | Start Event | Email-triggered workflow start |

---

## Process Variables

Define input/output variables for the workflow at the process level.

### Location
```xml
<bpmn:process id="my_workflow">
  <bpmn:extensionElements>
    <periscope:processVariables>
      <!-- variables here -->
    </periscope:processVariables>
  </bpmn:extensionElements>
</bpmn:process>
```

### ProcessVariable Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | String | Yes | Variable identifier |
| `type` | String | Yes | Data type: `string`, `number`, `boolean`, `object`, `array` |
| `required` | Boolean | No | Whether variable is required (default: false) |
| `isInput` | Boolean | No | Whether variable is a workflow input (default: false) |
| `defaultValue` | String | No | Default value if not provided |
| `description` | String | No | Human-readable description |
| `constraints` | String | No | Validation constraints (JSON) |

### Example

```xml
<periscope:processVariables>
  <periscope:processVariable
    name="document_id"
    type="string"
    required="true"
    isInput="true"
    description="Unique document identifier" />
  <periscope:processVariable
    name="extracted_data"
    type="object"
    required="false"
    description="AI-extracted structured data" />
</periscope:processVariables>
```

---

## AI Agent Configuration

Configure PydanticAI agent execution for Service Tasks.

### Location
```xml
<bpmn:serviceTask id="analyze_document" name="Analyze Document">
  <bpmn:extensionElements>
    <periscope:aIAgentConfiguration>
      <!-- configuration here -->
    </periscope:aIAgentConfiguration>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

### AIAgentConfiguration Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `agentId` | String | Yes | Registered agent identifier |
| `agentType` | String | No | Agent category: `extraction`, `classification`, `validation`, `generation` |
| `modelProvider` | String | No | LLM provider: `openai`, `anthropic`, `google` |
| `modelName` | String | No | Model identifier: `gpt-4o`, `claude-3-5-sonnet`, `gemini-pro` |
| `prompt` | String | No | System prompt override |

### Nested Elements

#### InputMapping
Maps process variables to agent inputs.

```xml
<periscope:inputMapping source="document_url" target="file_url" />
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `source` | String | Process variable name |
| `target` | String | Agent input parameter name |

#### OutputMapping
Maps agent outputs to process variables.

```xml
<periscope:outputMapping variable="extracted_data" errorVariable="extraction_error" />
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `variable` | String | Target process variable for result |
| `errorVariable` | String | Target variable for errors |

#### BusinessContext
Include additional context for the agent.

```xml
<periscope:businessContext
  includeWorkflowContext="true"
  includeUserPermissions="true"
  includeComplianceLevel="false" />
```

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `includeWorkflowContext` | Boolean | true | Include workflow execution context |
| `includeUserPermissions` | Boolean | true | Include user role/permission info |
| `includeComplianceLevel` | Boolean | false | Include compliance requirements |

#### AdvancedSettings
Fine-tune agent behavior.

```xml
<periscope:advancedSettings
  temperature="0.2"
  maxTokens="4000"
  timeoutSeconds="120"
  enableFallback="true"
  enableStreaming="true"
  requireHumanValidation="false" />
```

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `temperature` | String | - | LLM temperature (0.0-1.0) |
| `maxTokens` | String | - | Maximum response tokens |
| `timeoutSeconds` | String | 300 | Execution timeout |
| `enableFallback` | Boolean | false | Enable fallback model on failure |
| `enableStreaming` | Boolean | true | Stream responses |
| `requireHumanValidation` | Boolean | false | Require human review of output |

#### StructuredOutput
Define expected output schema for type-safe responses.

```xml
<periscope:structuredOutput enabled="true" strictMode="true">
  <periscope:outputField name="vendor_name" fieldType="string" required="true" />
  <periscope:outputField name="total_amount" fieldType="number" required="true" />
  <periscope:outputField name="line_items" fieldType="array" itemType="object" required="false" />
  <periscope:outputField
    name="category"
    fieldType="enum"
    enumValues="invoice,contract,report,other"
    required="true" />
</periscope:structuredOutput>
```

**StructuredOutput Attributes:**
| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | Boolean | false | Enable structured output |
| `strictMode` | Boolean | true | Enforce schema strictly |
| `jsonSchema` | String | - | Full JSON schema (alternative to fields) |

**OutputField Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | String | Field name |
| `fieldType` | String | Type: `string`, `number`, `boolean`, `object`, `array`, `enum` |
| `required` | Boolean | Whether field is required |
| `description` | String | Field description for LLM |
| `enumValues` | String | Comma-separated enum values |
| `itemType` | String | Array item type |
| `nestedFields` | OutputField[] | Nested fields for objects |

#### ValidationConfig
Configure output validation rules.

```xml
<periscope:validationConfig enabled="true" documentType="invoice" strictness="high">
  <periscope:validationRules
    dataCompleteness="true"
    formatValidation="true"
    crossReference="false"
    businessCompliance="true" />
</periscope:validationConfig>
```

**ValidationConfig Attributes:**
| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | Boolean | false | Enable validation |
| `documentType` | String | - | Expected document type |
| `strictness` | String | medium | Validation strictness: `low`, `medium`, `high` |

**ValidationRules Attributes:**
| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataCompleteness` | Boolean | true | Check all required fields present |
| `formatValidation` | Boolean | true | Validate data formats |
| `crossReference` | Boolean | false | Cross-reference with external data |
| `businessCompliance` | Boolean | false | Check business rules |
| `customRules` | String | - | Custom validation logic (JSON) |

### Complete Example

```xml
<bpmn:serviceTask id="extract_invoice" name="Extract Invoice Data">
  <bpmn:extensionElements>
    <periscope:aIAgentConfiguration
      agentId="invoice-processor"
      agentType="extraction"
      modelProvider="openai"
      modelName="gpt-4o"
      prompt="Extract all invoice details including vendor, amounts, and line items.">

      <periscope:inputMapping source="document_url" target="file_url" />
      <periscope:inputMapping source="document_id" target="doc_id" />

      <periscope:outputMapping variable="invoice_data" errorVariable="extraction_error" />

      <periscope:businessContext
        includeWorkflowContext="true"
        includeUserPermissions="false" />

      <periscope:advancedSettings
        temperature="0.1"
        maxTokens="4000"
        timeoutSeconds="90"
        enableFallback="true" />

      <periscope:structuredOutput enabled="true" strictMode="true">
        <periscope:outputField name="vendor_name" fieldType="string" required="true" />
        <periscope:outputField name="invoice_number" fieldType="string" required="true" />
        <periscope:outputField name="invoice_date" fieldType="string" required="true" />
        <periscope:outputField name="total_amount" fieldType="number" required="true" />
        <periscope:outputField name="currency" fieldType="string" required="true" />
        <periscope:outputField name="line_items" fieldType="array" itemType="object" />
      </periscope:structuredOutput>

      <periscope:validationConfig enabled="true" documentType="invoice" strictness="high">
        <periscope:validationRules
          dataCompleteness="true"
          formatValidation="true"
          businessCompliance="true" />
      </periscope:validationConfig>

    </periscope:aIAgentConfiguration>
  </bpmn:extensionElements>
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>flow2</bpmn:outgoing>
</bpmn:serviceTask>
```

---

## Task Definition (User Tasks)

Configure human task assignment, forms, and notifications.

### Location
```xml
<bpmn:userTask id="review_document" name="Review Document">
  <bpmn:extensionElements>
    <periscope:taskDefinition>
      <!-- configuration here -->
    </periscope:taskDefinition>
  </bpmn:extensionElements>
</bpmn:userTask>
```

### TaskDefinition Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `assignee` | String | No | User/variable for assignment: `${variable}` or `user@email.com` |
| `priority` | Integer | No | Priority level: 1 (highest) to 5 (lowest) |
| `outputVariable` | String | No | Variable to store task result |

### Nested Elements

#### FormData
Define the input form for the task.

```xml
<periscope:formData>
  <periscope:field name="approved" type="boolean" required="true" label="Approve Request?" />
  <periscope:field name="comments" type="text" required="false" label="Comments" />
  <periscope:field name="budget_code" type="string" required="true" label="Budget Code" />
</periscope:formData>
```

**Field Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | String | Field identifier |
| `type` | String | Input type: `string`, `text`, `boolean`, `number`, `date`, `select`, `object` |
| `required` | Boolean | Whether field is required |
| `label` | String | Display label |

#### EmailNotification
Configure email notifications for the task.

```xml
<periscope:emailNotification
  enabled="true"
  onAssignment="true"
  onDeadline="true"
  reminderInterval="PT4H"
  subject="Task Assigned: ${task_name}"
  template="task/assigned">
  <periscope:recipients recipientType="assignee" value="${assignee}" />
  <periscope:recipients recipientType="role" value="manager" />
</periscope:emailNotification>
```

**EmailNotification Attributes:**
| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | Boolean | false | Enable notifications |
| `onAssignment` | Boolean | true | Send on task assignment |
| `onDeadline` | Boolean | false | Send on deadline approach |
| `reminderInterval` | String | - | ISO 8601 duration for reminders |
| `subject` | String | - | Email subject (supports variables) |
| `template` | String | - | Email template: `task/assigned`, `task/due_reminder`, `task/escalated` |

**Recipients Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `recipientType` | String | Type: `assignee`, `role`, `email`, `variable` |
| `value` | String | Recipient value based on type |

### Complete Example

```xml
<bpmn:userTask id="manager_approval" name="Manager Approval">
  <bpmn:extensionElements>
    <periscope:taskDefinition assignee="${requester_manager}" priority="2" outputVariable="approval_result">
      <periscope:formData>
        <periscope:field name="approved" type="boolean" required="true" label="Approve Request?" />
        <periscope:field name="comments" type="text" required="false" label="Comments" />
        <periscope:field name="budget_code" type="string" required="true" label="Budget Code" />
      </periscope:formData>
      <periscope:emailNotification
        enabled="true"
        onAssignment="true"
        onDeadline="true"
        reminderInterval="PT4H"
        subject="Approval Required: ${request_id}"
        template="task/assigned">
        <periscope:recipients recipientType="assignee" value="${requester_manager}" />
      </periscope:emailNotification>
    </periscope:taskDefinition>
  </bpmn:extensionElements>
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>flow2</bpmn:outgoing>
</bpmn:userTask>
```

---

## Send Task Configuration

Configure email sending for Send Tasks.

### Location
```xml
<bpmn:sendTask id="send_notification" name="Send Notification">
  <bpmn:extensionElements>
    <periscope:sendTaskConfiguration>
      <!-- configuration here -->
    </periscope:sendTaskConfiguration>
  </bpmn:extensionElements>
</bpmn:sendTask>
```

### SendTaskConfiguration Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `subject` | String | Yes | Email subject (supports variables) |
| `template` | String | No | Template: `send_task/notification`, `send_task/alert`, `send_task/confirmation` |
| `bodyHtml` | String | No | HTML body (if not using template) |
| `bodyText` | String | No | Plain text body |
| `replyTo` | String | No | Reply-to address |
| `priority` | String | No | Priority: `low`, `normal`, `high` |
| `trackOpens` | Boolean | No | Track email opens |
| `trackClicks` | Boolean | No | Track link clicks |
| `outputVariable` | String | No | Variable for send result |

### Nested Elements

#### Recipients (to, cc, bcc)
```xml
<periscope:to recipientType="variable" value="${requester_email}" />
<periscope:to recipientType="email" value="admin@company.com" />
<periscope:cc recipientType="role" value="finance_team" />
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `recipientType` | String | Type: `email`, `variable`, `role`, `assignee` |
| `value` | String | Recipient value based on type |

#### Attachments
```xml
<periscope:attachments sourceType="variable" source="${report_url}" filename="report.pdf" mimeType="application/pdf" />
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `sourceType` | String | Source type: `variable`, `url`, `inline` |
| `source` | String | Attachment source |
| `filename` | String | Attachment filename |
| `mimeType` | String | MIME type |

### Complete Example

```xml
<bpmn:sendTask id="send_approval" name="Send Approval Notification">
  <bpmn:extensionElements>
    <periscope:sendTaskConfiguration
      subject="Request ${request_id} Approved"
      template="send_task/notification"
      priority="normal"
      trackOpens="true"
      outputVariable="email_result">
      <periscope:to recipientType="variable" value="${requester_email}" />
      <periscope:cc recipientType="role" value="finance_team" />
    </periscope:sendTaskConfiguration>
  </bpmn:extensionElements>
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>flow2</bpmn:outgoing>
</bpmn:sendTask>
```

---

## Script Task Configuration

Configure sandboxed function execution for Script Tasks.

### Location
```xml
<bpmn:scriptTask id="process_data" name="Process Data">
  <bpmn:extensionElements>
    <periscope:scriptTaskConfiguration>
      <!-- configuration here -->
    </periscope:scriptTaskConfiguration>
  </bpmn:extensionElements>
</bpmn:scriptTask>
```

### ScriptTaskConfiguration Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `functionId` | String | Yes | Registered function identifier |
| `functionName` | String | Yes | Function name to execute |
| `version` | Integer | No | Function version (default: latest) |
| `description` | String | No | Human-readable description |
| `outputVariable` | String | No | Variable for function result |

### Nested Elements

#### ScriptTaskInputMapping
```xml
<periscope:scriptTaskInputMapping source="extracted_text" target="text_content" mappingType="variable" />
```

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | String | - | Source variable or literal |
| `target` | String | - | Function parameter name |
| `mappingType` | String | variable | Type: `variable`, `literal`, `expression` |

### Complete Example

```xml
<bpmn:scriptTask id="calculate_totals" name="Calculate Totals">
  <bpmn:extensionElements>
    <periscope:scriptTaskConfiguration
      functionId="financial-calculator"
      functionName="calculate_invoice_totals"
      version="1"
      description="Calculate tax and total amounts"
      outputVariable="calculated_totals">
      <periscope:scriptTaskInputMapping source="line_items" target="items" mappingType="variable" />
      <periscope:scriptTaskInputMapping source="tax_rate" target="tax_rate" mappingType="variable" />
    </periscope:scriptTaskConfiguration>
  </bpmn:extensionElements>
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>flow2</bpmn:outgoing>
</bpmn:scriptTask>
```

---

## Email Trigger Configuration

Configure email-triggered workflow starts.

### Location
```xml
<bpmn:startEvent id="email_received" name="Email Received">
  <bpmn:extensionElements>
    <periscope:emailTriggerConfiguration>
      <!-- configuration here -->
    </periscope:emailTriggerConfiguration>
  </bpmn:extensionElements>
  <bpmn:messageEventDefinition />
</bpmn:startEvent>
```

### EmailTriggerConfiguration Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | Boolean | true | Enable email trigger |
| `addressPattern` | String | - | Regex pattern for trigger email address |
| `subjectPattern` | String | - | Regex pattern for subject matching |
| `allowedSenders` | String | - | Comma-separated allowed sender patterns |
| `blockedSenders` | String | - | Comma-separated blocked sender patterns |
| `extractAttachments` | Boolean | true | Extract email attachments |
| `maxAttachmentSizeMb` | Integer | 10 | Maximum attachment size in MB |
| `autoReply` | Boolean | false | Send automatic reply |
| `autoReplyTemplate` | String | - | Template for auto-reply |

### Complete Example

```xml
<bpmn:startEvent id="invoice_email" name="Invoice Email Received">
  <bpmn:extensionElements>
    <periscope:emailTriggerConfiguration
      enabled="true"
      addressPattern="invoices\+.*@company\.com"
      subjectPattern="(?i)invoice|bill|payment"
      allowedSenders="*@vendor.com,accounting@*"
      blockedSenders="*@spam.com"
      extractAttachments="true"
      maxAttachmentSizeMb="25"
      autoReply="true"
      autoReplyTemplate="email/invoice-received" />
  </bpmn:extensionElements>
  <bpmn:outgoing>flow1</bpmn:outgoing>
  <bpmn:messageEventDefinition id="MessageEventDefinition_1" />
</bpmn:startEvent>
```

---

## Variable Interpolation

Throughout Periscope extensions, you can use variable interpolation with `${variable_name}` syntax:

```xml
<!-- In attributes -->
<periscope:taskDefinition assignee="${requester_manager}" />

<!-- In email subjects -->
<periscope:sendTaskConfiguration subject="Request ${request_id} - ${status}" />

<!-- In recipients -->
<periscope:to recipientType="variable" value="${requester_email}" />
```

Variables are resolved at runtime from:
1. Process variables defined in `processVariables`
2. Workflow execution context
3. Task completion outputs

---

## Best Practices

### 1. Always Define Process Variables
Document all inputs and outputs at the process level:
```xml
<periscope:processVariables>
  <periscope:processVariable name="input_var" type="string" required="true" isInput="true" />
  <periscope:processVariable name="output_var" type="object" required="false" />
</periscope:processVariables>
```

### 2. Use Structured Output for AI Agents
Enable type-safe responses:
```xml
<periscope:structuredOutput enabled="true" strictMode="true">
  <periscope:outputField name="result" fieldType="object" required="true" />
</periscope:structuredOutput>
```

### 3. Configure Error Variables
Always capture potential errors:
```xml
<periscope:outputMapping variable="result" errorVariable="error" />
```

### 4. Set Appropriate Timeouts
Configure timeouts based on expected execution time:
```xml
<periscope:advancedSettings timeoutSeconds="120" enableFallback="true" />
```

### 5. Use Email Templates
Prefer templates over inline content for maintainability:
```xml
<periscope:sendTaskConfiguration template="send_task/notification" />
```
