name: Feature Request
description: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: ["type:feature", "status:needs-clarification"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        # Feature Request

        Thank you for suggesting an enhancement! Please fill out this form clearly.

  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: Describe the problem or limitation you want to address
      placeholder: |
        What problem does this feature solve?
        What is the current workaround (if any)?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe how you'd like this feature to work
      placeholder: |
        How should this feature work?
        What should the user experience be?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Approaches
      description: Have you considered other solutions?
      placeholder: |
        What other approaches did you consider?
        Why is your approach better?

  - type: dropdown
    id: area
    attributes:
      label: Area
      description: Which part of the system does this affect?
      options:
        - Backend
        - Frontend
        - Data Processing
        - Documentation
        - CI/CD
        - Other
    validations:
      required: true

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: How urgent is this feature?
      options:
        - Low
        - Medium
        - High
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have searched existing issues
          required: true
        - label: This is not a duplicate
          required: true
        - label: I can help implement this
