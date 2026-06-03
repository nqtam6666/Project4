import os
import json
from flask import Blueprint, jsonify, render_template_string

nqt_api_docs_bp = Blueprint('nqt_api_docs', __name__)

# HTML template for Swagger UI supporting both Dark & Light themes matching G6 Gym design system
SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>G6 Gym API Documentation</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
  <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@5.11.0/favicon-32x32.png" sizes="32x32" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
  <style>
    /* Design Tokens (CSS Variables) supporting Dark & Light Modes */
    :root {
      --bg-color: #0A0A0F;
      --elevation-bg: #12121A;
      --input-bg: #1C1C28;
      --text-main: #F5F5F0;
      --text-muted: #A1A1AA;
      --border-color: rgba(255, 255, 255, 0.06);
      --border-color-strong: rgba(255, 255, 255, 0.12);
      --accent-color: #C8F135;
      --accent-hover: #D6FA4A;
      --table-header-color: #A1A1AA;
      --pre-bg: #0A0A0F;
      --btn-bg: #1C1C28;
      --btn-hover: #252535;
      --shadow-color: rgba(0, 0, 0, 0.5);
      --tag-border: rgba(255, 255, 255, 0.08);
      --lock-color: #A1A1AA;
      --syntax-string: #22C55E;
    }

    body.light-mode {
      --bg-color: #F3F4F6;
      --elevation-bg: #FFFFFF;
      --input-bg: #E5E7EB;
      --text-main: #111827;
      --text-muted: #4B5563;
      --border-color: rgba(0, 0, 0, 0.08);
      --border-color-strong: rgba(0, 0, 0, 0.15);
      --accent-color: #74B816; /* Clean readable green for light backgrounds */
      --accent-hover: #5F9610;
      --table-header-color: #374151;
      --pre-bg: #F9FAFB;
      --btn-bg: #E5E7EB;
      --btn-hover: #D1D5DB;
      --shadow-color: rgba(0, 0, 0, 0.06);
      --tag-border: rgba(0, 0, 0, 0.1);
      --lock-color: #4B5563;
      --syntax-string: #16A34A; /* Deep forest green for high contrast on light backgrounds */
    }

    /* Global Reset & Base Fonts */
    body {
      background-color: var(--bg-color) !important;
      margin: 0;
      font-family: 'Inter', sans-serif !important;
      transition: background-color 0.3s ease, color 0.3s ease;
    }
    
    /* Floating Theme Toggle Button */
    .theme-toggle-btn {
      position: fixed;
      top: 12px;
      right: 20px;
      z-index: 9999;
      background-color: var(--elevation-bg);
      border: 1px solid var(--border-color-strong);
      color: var(--text-main);
      width: 42px;
      height: 42px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px var(--shadow-color);
      transition: all 0.25s ease;
    }
    
    .theme-toggle-btn:hover {
      transform: scale(1.08);
      border-color: var(--accent-color);
      box-shadow: 0 0 12px var(--accent-color);
    }

    .theme-toggle-btn svg {
      stroke: var(--text-main);
      fill: none;
    }

    /* Topbar Custom Styling */
    .swagger-ui .topbar {
      background-color: var(--elevation-bg) !important;
      border-bottom: 1px solid var(--border-color) !important;
      padding: 15px 0 !important;
      box-shadow: 0 4px 30px var(--shadow-color) !important;
    }
    
    .swagger-ui .topbar a span {
      color: var(--text-main) !important;
      font-weight: 800 !important;
      font-family: 'Space Grotesk', sans-serif !important;
      text-transform: uppercase;
      letter-spacing: 1.5px;
    }
    
    .swagger-ui .topbar .download-url-wrapper input[type=text] {
      background-color: var(--input-bg) !important;
      border: 1px solid var(--border-color) !important;
      border-radius: 8px !important;
      color: var(--text-main) !important;
      font-family: 'JetBrains Mono', monospace !important;
    }
    
    .swagger-ui .topbar .download-url-button {
      background-color: var(--accent-color) !important;
      color: #0A0A0F !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: bold !important;
      border-radius: 8px !important;
    }
    
    /* Global Container */
    .swagger-ui {
      background-color: var(--bg-color) !important;
      color: var(--text-main) !important;
      font-family: 'Inter', sans-serif !important;
    }
    
    /* Info Block */
    .swagger-ui .info {
      margin: 40px 0 !important;
    }
    
    .swagger-ui .info .title {
      font-family: 'Space Grotesk', sans-serif !important;
      color: var(--text-main) !important;
      font-weight: 800 !important;
      font-size: 2.8em !important;
      letter-spacing: -0.5px !important;
    }
    
    .swagger-ui .info .title small {
      background-color: var(--accent-color) !important;
      color: #0A0A0F !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: bold !important;
      border-radius: 6px !important;
      padding: 4px 8px !important;
      font-size: 0.4em !important;
      vertical-align: middle !important;
      margin-left: 10px !important;
    }
    
    .swagger-ui .info p,
    .swagger-ui .info li,
    .swagger-ui .info table,
    .swagger-ui .info a {
      color: var(--text-muted) !important;
      font-size: 14px !important;
      line-height: 1.6 !important;
    }
    
    .swagger-ui .info a {
      color: var(--accent-color) !important;
      text-decoration: none !important;
      font-weight: 500 !important;
    }
    
    .swagger-ui .info a:hover {
      text-decoration: underline !important;
    }
    
    /* Scheme and Servers Container */
    .swagger-ui .scheme-container {
      background-color: var(--elevation-bg) !important;
      border: 1px solid var(--border-color) !important;
      border-radius: 16px !important;
      box-shadow: 0 10px 40px var(--shadow-color) !important;
      padding: 24px !important;
      margin: 30px 0 !important;
    }
    
    .swagger-ui .scheme-container label {
      color: var(--text-muted) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 12px !important;
      text-transform: uppercase !important;
      letter-spacing: 1px !important;
    }
    
    .swagger-ui select {
      background-color: var(--input-bg) !important;
      color: var(--text-main) !important;
      border: 1px solid var(--border-color) !important;
      border-radius: 8px !important;
      padding: 8px 12px !important;
      font-family: 'Inter', sans-serif !important;
      font-size: 13px !important;
      outline: none !important;
    }
    
    .swagger-ui select:focus {
      border-color: var(--accent-color) !important;
    }
    
    /* Tag Sections */
    .swagger-ui .opblock-tag {
      color: var(--text-main) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: 700 !important;
      font-size: 1.4em !important;
      border-bottom: 1px solid var(--border-color) !important;
      padding: 15px 0 !important;
      letter-spacing: -0.2px !important;
    }
    
    .swagger-ui .opblock-tag small {
      color: var(--text-muted) !important;
      font-family: 'Inter', sans-serif !important;
      font-size: 0.6em !important;
      margin-left: 10px !important;
    }
    
    /* Operations Cards (opblocks) */
    .swagger-ui .opblock {
      border-radius: 16px !important;
      border: 1px solid var(--border-color) !important;
      box-shadow: 0 4px 20px var(--shadow-color) !important;
      overflow: hidden !important;
      background-color: var(--elevation-bg) !important;
      margin-bottom: 16px !important;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .swagger-ui .opblock:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 8px 30px var(--shadow-color) !important;
      border-color: var(--border-color-strong) !important;
    }
    
    .swagger-ui .opblock .opblock-summary {
      border-bottom: 1px solid var(--border-color) !important;
      padding: 12px 20px !important;
      background-color: transparent !important;
    }
    
    /* HTTP Methods Styling */
    .swagger-ui .opblock-summary-method {
      border-radius: 8px !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: 700 !important;
      font-size: 12px !important;
      text-transform: uppercase !important;
      letter-spacing: 1px !important;
      padding: 6px 12px !important;
      min-width: 80px !important;
      text-align: center !important;
    }
    
    /* Colors for distinct methods */
    .swagger-ui .opblock.opblock-get {
      border-left: 4px solid #3B82F6 !important;
    }
    .swagger-ui .opblock.opblock-get .opblock-summary-method {
      background-color: rgba(59, 130, 246, 0.15) !important;
      color: #3B82F6 !important;
      border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    .swagger-ui .opblock.opblock-post {
      border-left: 4px solid #22C55E !important;
    }
    .swagger-ui .opblock.opblock-post .opblock-summary-method {
      background-color: rgba(34, 197, 94, 0.15) !important;
      color: #22C55E !important;
      border: 1px solid rgba(34, 197, 94, 0.3) !important;
    }
    
    .swagger-ui .opblock.opblock-put {
      border-left: 4px solid #F59E0B !important;
    }
    .swagger-ui .opblock.opblock-put .opblock-summary-method {
      background-color: rgba(245, 158, 11, 0.15) !important;
      color: #F59E0B !important;
      border: 1px solid rgba(245, 158, 11, 0.3) !important;
    }
    
    .swagger-ui .opblock.opblock-delete {
      border-left: 4px solid #EF4444 !important;
    }
    .swagger-ui .opblock.opblock-delete .opblock-summary-method {
      background-color: rgba(239, 68, 68, 0.15) !important;
      color: #EF4444 !important;
      border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Highly specific path and description rules to override Swagger UI method colors */
    .swagger-ui .opblock.opblock-get .opblock-summary-path,
    .swagger-ui .opblock.opblock-get .opblock-summary-path a,
    .swagger-ui .opblock.opblock-post .opblock-summary-path,
    .swagger-ui .opblock.opblock-post .opblock-summary-path a,
    .swagger-ui .opblock.opblock-put .opblock-summary-path,
    .swagger-ui .opblock.opblock-put .opblock-summary-path a,
    .swagger-ui .opblock.opblock-delete .opblock-summary-path,
    .swagger-ui .opblock.opblock-delete .opblock-summary-path a,
    .swagger-ui .opblock-summary-path,
    .swagger-ui .opblock-summary-path a,
    .swagger-ui .opblock-summary-path__deprecated,
    .swagger-ui .opblock-summary-operation-id {
      color: var(--text-main) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 14px !important;
      font-weight: 500 !important;
      text-decoration: none !important;
    }
    
    .swagger-ui .opblock.opblock-get .opblock-summary-description,
    .swagger-ui .opblock.opblock-post .opblock-summary-description,
    .swagger-ui .opblock.opblock-put .opblock-summary-description,
    .swagger-ui .opblock.opblock-delete .opblock-summary-description,
    .swagger-ui .opblock-summary-description {
      color: var(--text-muted) !important;
      font-family: 'Inter', sans-serif !important;
      font-size: 13px !important;
    }

    .swagger-ui .authorization__btn,
    .swagger-ui .opblock .opblock-summary .authorization__btn {
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      padding: 0 10px !important;
    }

    .swagger-ui .authorization__btn svg,
    .swagger-ui .authorization__btn svg path,
    .swagger-ui .opblock .opblock-summary .authorization__btn svg,
    .swagger-ui .opblock .opblock-summary .authorization__btn svg path,
    .swagger-ui .opblock .opblock-summary .arrow svg,
    .swagger-ui .opblock .opblock-summary .arrow svg path {
      fill: var(--lock-color) !important;
    }
    
    .swagger-ui .authorization__btn svg.unlocked,
    .swagger-ui .authorization__btn svg.unlocked path {
      fill: var(--accent-color) !important;
    }
    
    .swagger-ui .authorization__btn svg.locked,
    .swagger-ui .authorization__btn svg.locked path {
      fill: #EF4444 !important;
    }
    
    /* Section Headers (the generic gray bars) */
    .swagger-ui .opblock .opblock-section-header {
      background-color: var(--border-color) !important;
      border-bottom: 1px solid var(--border-color) !important;
      padding: 12px 20px !important;
      box-shadow: none !important;
    }
    
    .swagger-ui .opblock .opblock-section-header h4 {
      color: var(--text-main) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: 600 !important;
      text-transform: uppercase !important;
      letter-spacing: 1px !important;
      font-size: 12px !important;
    }
    
    /* Tables Styling */
    .swagger-ui table {
      background-color: transparent !important;
    }
    
    .swagger-ui table thead tr td,
    .swagger-ui table thead tr th {
      color: var(--table-header-color) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      text-transform: uppercase !important;
      letter-spacing: 0.5px !important;
      font-size: 11px !important;
      border-bottom: 1px solid var(--border-color) !important;
      padding: 12px 20px !important;
    }
    
    .swagger-ui table tbody tr td {
      border-bottom: 1px solid var(--border-color) !important;
      padding: 15px 20px !important;
      background-color: transparent !important;
      vertical-align: top !important;
    }
    
    .swagger-ui .parameter__name {
      color: var(--text-main) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 13px !important;
      font-weight: 700 !important;
    }
    
    .swagger-ui .parameter__name.required:after {
      color: #EF4444 !important;
    }
    
    .swagger-ui .parameter__type {
      color: var(--accent-color) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 11px !important;
    }
    
    .swagger-ui .parameter__in {
      color: var(--text-muted) !important;
      font-family: 'Inter', sans-serif !important;
      font-style: normal !important;
      font-size: 11px !important;
    }
    
    .swagger-ui .parameter__description {
      color: var(--text-muted) !important;
      font-size: 13px !important;
    }
    
    .swagger-ui .response-col_status {
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: bold !important;
      color: var(--text-main) !important;
    }
    
    .swagger-ui .response-col_description {
      color: var(--text-muted) !important;
    }
    
    /* Code blocks & Pre-formatted areas */
    .swagger-ui pre,
    .swagger-ui .opblock-body pre.microlight {
      background-color: var(--pre-bg) !important;
      border: 1px solid var(--border-color) !important;
      border-radius: 12px !important;
      padding: 16px !important;
      box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    .swagger-ui code,
    .swagger-ui pre,
    .swagger-ui .opblock-body pre.microlight code {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 13px !important;
      color: var(--text-main) !important;
      line-height: 1.5 !important;
    }

    /* Style syntax highlighted strings */
    .swagger-ui .microlight .str,
    .swagger-ui pre .str,
    .swagger-ui code .str,
    .swagger-ui .hljs-string,
    .swagger-ui pre .hljs-string,
    .swagger-ui code .hljs-string {
      color: var(--syntax-string) !important;
    }
    
    /* Buttons */
    .swagger-ui .btn {
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 12px !important;
      font-weight: bold !important;
      text-transform: uppercase !important;
      letter-spacing: 1px !important;
      border-radius: 8px !important;
      padding: 6px 16px !important;
      transition: all 0.2s ease !important;
      box-shadow: none !important;
      background-color: var(--btn-bg) !important;
      color: var(--text-main) !important;
      border: 1px solid var(--border-color) !important;
    }
    
    .swagger-ui .btn:hover {
      background-color: var(--btn-hover) !important;
    }
    
    /* Execute / Try Out button */
    .swagger-ui .btn.execute {
      background-color: var(--accent-color) !important;
      color: #0A0A0F !important;
      border-color: var(--accent-color) !important;
    }
    
    .swagger-ui .btn.execute:hover {
      background-color: var(--accent-hover) !important;
      transform: scale(1.02) !important;
      box-shadow: 0 0 15px var(--accent-color) !important;
    }
    
    /* Authorize Button */
    .swagger-ui .btn.authorize {
      background-color: transparent !important;
      color: var(--accent-color) !important;
      border-color: var(--accent-color) !important;
    }
    
    .swagger-ui .btn.authorize:hover {
      background-color: rgba(200, 241, 53, 0.08) !important;
    }
    
    .swagger-ui .btn.authorize svg {
      fill: var(--accent-color) !important;
    }
    
    .swagger-ui .btn.cancel {
      background-color: transparent !important;
      color: #EF4444 !important;
      border-color: rgba(239, 68, 68, 0.4) !important;
    }
    
    .swagger-ui .btn.cancel:hover {
      background-color: rgba(239, 68, 68, 0.08) !important;
      border-color: #EF4444 !important;
    }
    
    /* Inputs, Textareas, Selects */
    .swagger-ui input[type=text],
    .swagger-ui textarea {
      background-color: var(--elevation-bg) !important;
      color: var(--text-main) !important;
      border: 1px solid var(--border-color) !important;
      border-radius: 8px !important;
      padding: 10px 14px !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 13px !important;
      outline: none !important;
      transition: border-color 0.2s ease !important;
    }
    
    .swagger-ui input[type=text]:focus,
    .swagger-ui textarea:focus {
      border-color: var(--accent-color) !important;
      box-shadow: 0 0 8px var(--accent-color) !important;
    }
    
    .swagger-ui .body-param__text {
      background-color: var(--pre-bg) !important;
    }
    
    /* Models Section */
    .swagger-ui section.models {
      border: 1px solid var(--border-color) !important;
      border-radius: 16px !important;
      background-color: var(--elevation-bg) !important;
      overflow: hidden !important;
      margin: 40px 0 !important;
    }
    
    .swagger-ui section.models h4 {
      border-bottom: 1px solid var(--border-color) !important;
      padding: 16px 20px !important;
      background-color: var(--border-color) !important;
      color: var(--text-main) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      letter-spacing: 1px !important;
    }
    
    .swagger-ui section.models .model-container {
      background-color: transparent !important;
      border: none !important;
      margin: 0 !important;
      padding: 12px 20px !important;
      border-bottom: 1px solid var(--border-color) !important;
    }
    
    .swagger-ui section.models .model-container:last-child {
      border-bottom: none !important;
      padding-bottom: 0 !important;
    }
    
    .swagger-ui .model-box {
      background-color: var(--pre-bg) !important;
      border: 1px solid var(--border-color) !important;
      border-radius: 8px !important;
      padding: 12px !important;
    }
    
    .swagger-ui .model-title {
      font-family: 'Space Grotesk', sans-serif !important;
      color: var(--text-main) !important;
      font-weight: 600 !important;
    }
    
    .swagger-ui .prop-type {
      color: var(--accent-color) !important;
    }
    
    .swagger-ui .prop-format {
      color: var(--text-muted) !important;
    }
    
    /* Dialog/Authorize Modal */
    .swagger-ui .dialog-ux .modal-ux {
      background-color: var(--elevation-bg) !important;
      border: 1px solid var(--border-color-strong) !important;
      box-shadow: 0 20px 50px var(--shadow-color) !important;
      border-radius: 16px !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-header {
      border-bottom: 1px solid var(--border-color) !important;
      padding: 20px !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-header h3 {
      color: var(--text-main) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: 700 !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-content {
      padding: 20px !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-content h4 {
      color: var(--text-muted) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      text-transform: uppercase !important;
      letter-spacing: 0.5px !important;
      font-size: 12px !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-header .close-modal {
      fill: var(--text-main) !important;
    }
    
    .swagger-ui .auth-container {
      border-bottom: 1px solid var(--border-color) !important;
      padding-bottom: 20px !important;
    }
    
    .swagger-ui .auth-container:last-child {
      border-bottom: none !important;
      padding-bottom: 0 !important;
    }
    
    /* Fix tab controls in Try it out body */
    .swagger-ui .tab {
      display: flex !important;
      padding: 0 !important;
      margin: 0 0 10px 0 !important;
      list-style: none !important;
      border-bottom: 1px solid var(--border-color) !important;
    }
    
    .swagger-ui .tab li {
      margin-right: 10px !important;
    }
    
    .swagger-ui .tab li button {
      background: transparent !important;
      border: none !important;
      color: var(--text-muted) !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-weight: 600 !important;
      padding: 8px 12px !important;
      cursor: pointer !important;
      font-size: 12px !important;
      text-transform: uppercase !important;
      letter-spacing: 0.5px !important;
    }
    
    .swagger-ui .tab li.active button {
      color: var(--accent-color) !important;
      border-bottom: 2px solid var(--accent-color) !important;
    }
  </style>
</head>
<body>
  <!-- Floating Toggle Button -->
  <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle Theme">
    <svg class="theme-icon-sun" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none;"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
    <svg class="theme-icon-moon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
  </button>

  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" charset="UTF-8"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-standalone-preset.js" charset="UTF-8"></script>
  <script>
    window.onload = function() {
      const ui = SwaggerUIBundle({
        url: "/api/nqt-openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "BaseLayout"
      });
      window.ui = ui;

      // Theme toggle functionality
      const toggleBtn = document.getElementById('theme-toggle');
      const sunIcon = toggleBtn.querySelector('.theme-icon-sun');
      const moonIcon = toggleBtn.querySelector('.theme-icon-moon');
      
      const savedTheme = localStorage.getItem('swagger-ui-theme') || 'dark';
      if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        sunIcon.style.display = 'block';
        moonIcon.style.display = 'none';
      }
      
      // Recolor microlight string spans (they use inline style so CSS can't override)
      const STRING_COLORS = {
        dark: '#22C55E',
        light: '#16A34A'
      };
      // microlight renders string spans with color:#22aa99 or similar teal — override all
      function patchMicrolightStrings() {
        const isLight = document.body.classList.contains('light-mode');
        const targetColor = isLight ? STRING_COLORS.light : STRING_COLORS.dark;
        // microlight string spans use inline color inside pre.microlight
        document.querySelectorAll('.swagger-ui pre.microlight span').forEach(function(span) {
          const col = span.style.color ? span.style.color.toLowerCase() : '';
          // Microlight uses teal colors for strings: #22aa99, #2aa198, #859900, etc.
          // We match any span that's NOT white/near-white and NOT a keyword red/orange
          if (col && col !== '' && !col.includes('rgb(245') && !col.includes('#f5') && !col.includes('#ef') && !col.includes('#e5') && !col.includes('rgb(239')) {
            span.style.color = targetColor;
          }
        });
      }

      // Observe DOM for new pre.microlight elements rendered by Swagger UI
      const observer = new MutationObserver(function() {
        patchMicrolightStrings();
      });
      observer.observe(document.getElementById('swagger-ui'), { childList: true, subtree: true });

      toggleBtn.onclick = function() {
        const isLight = document.body.classList.toggle('light-mode');
        localStorage.setItem('swagger-ui-theme', isLight ? 'light' : 'dark');
        if (isLight) {
          sunIcon.style.display = 'block';
          moonIcon.style.display = 'none';
        } else {
          sunIcon.style.display = 'none';
          moonIcon.style.display = 'block';
        }
        // Re-patch colors after theme switch
        patchMicrolightStrings();
      };
    };
  </script>
</body>
</html>
"""

@nqt_api_docs_bp.route('/api/nqt-api-docs', methods=['GET'])
def nqt_render_api_docs():
    return render_template_string(SWAGGER_UI_HTML)

@nqt_api_docs_bp.route('/api/nqt-openapi.json', methods=['GET'])
def nqt_get_openapi_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'nqt_openapi.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "OpenAPI spec file not found"}), 404
