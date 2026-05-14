name: Documentation Update
description: Report missing or unclear documentation
title: "[DOCS] "
labels: ["type:docs", "area:docs"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        # Documentation Issue

        Help us improve the documentation!

  - type: textarea
    id: issue
    attributes:
      label: Documentation Issue
      description: What is missing or unclear?
      placeholder: |
        Which page/file has an issue?
        What is missing or confusing?
        What should it be instead?
    validations:
      required: true

  - type: textarea
    id: location
    attributes:
      label: Location
      description: Where in the documentation is this issue?
      placeholder: |
        File: docs/backend/api.md
        Section: "Installation"
        Link: https://...

  - type: textarea
    id: suggestion
    attributes:
      label: Suggested Fix
      description: How should this be documented?
      placeholder: |
        The documentation should say:
        ...

  - type: dropdown
    id: doc_type
    attributes:
      label: Documentation Type
      options:
        - README
        - API Documentation
        - Architecture
        - Setup Guide
        - Workflow
        - Code Comments
        - Other
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I checked the latest documentation
          required: true
        - label: I searched for related docs issues
          required: true
