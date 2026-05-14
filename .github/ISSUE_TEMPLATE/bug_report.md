name: Bug Report
description: Report a bug or issue
title: "[BUG] "
labels: ["type:bug", "status:needs-triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        # Bug Report

        Thank you for reporting a bug! Please help us by filling out this form.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear and concise description of the bug
      placeholder: |
        What did you do?
        What did you expect to happen?
        What actually happened?
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Step-by-step instructions to reproduce
      placeholder: |
        1. Go to ...
        2. Click on ...
        3. See error ...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen instead?
      placeholder: The feature should...
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Relevant system information
      placeholder: |
        - OS: Windows/Mac/Linux
        - Python version: 3.10
        - Node version: 18
        - Browser: Chrome/Firefox/Safari

  - type: textarea
    id: logs
    attributes:
      label: Error Logs / Screenshots
      description: Paste error messages or attach screenshots
      placeholder: |
        ```
        Error stack trace here
        ```

  - type: dropdown
    id: area
    attributes:
      label: Affected Area
      description: Which part has the bug?
      options:
        - Backend
        - Frontend
        - Data Pipeline
        - Tests
        - CI/CD
        - Other
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I searched for existing issues
          required: true
        - label: This is not a duplicate
          required: true
        - label: I can reproduce the bug consistently
