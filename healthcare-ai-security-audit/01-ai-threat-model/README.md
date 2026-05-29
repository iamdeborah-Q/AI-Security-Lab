# AI Threat Model

## Overview

This phase focuses on identifying security risks within the DiagnosticAssist healthcare AI platform before production deployment.

## System Architecture

DiagnosticAssist analyzes medical images (X-rays, CT scans, and MRIs) using AI models and integrates with hospital EHR systems. The platform also provides an LLM-powered interface that allows clinicians to query diagnoses, patient history, and medical literature.

## Architecture Artifacts

* Architecture Diagram (`data-flow-diagram.svg`)
* Data Flow Diagram (`data-flow-diagram.md`)
* Mermaid Source (`data-flow-diagram.mmd`)

## Sensitive Data (PHI)

* Patient Records
* Medical Images
* Diagnostic Recommendations
* Clinical Conversations
* Authentication Credentials
* Session Tokens
* Audit Logs

## Data Flow

```text
Doctor Input
→ Authentication Service
→ LLM Interface
→ Image Analysis Pipeline
→ Model Inference
→ EHR Lookup
→ Diagnostic Output
→ Audit Logging
→ Doctor Response
```

## Assessment Objectives

* AI Threat Modeling
* STRIDE Analysis
* MITRE ATLAS Mapping
* Trust Boundary Identification
* Attack Surface Analysis
* Risk Assessment

## Deliverables

* Architecture Review
* Data Flow Analysis
* Trust Boundaries
* STRIDE Threat Model
* Risk Matrix
* Security Recommendations

```
```
  GNU nano 8.6                                                                                                   

