# Frappe INT - Enterprise Integration Platform
## VIBE Coding Specification Document v1.0

> **Project Codename**: INT (Integration)  
> **Framework**: Frappe Framework  
> **Target**: Enterprise-grade marketplace integration platform  
> **Positioning**: Zapier UX + Stockmount depth + AI-native automation

---

## Executive Summary

INT, Türkiye'nin ilk enterprise-grade, AI-native marketplace entegrasyon platformudur. Mevcut PIM (Product Information Management) uygulamasıyla entegre çalışarak, pazaryerleri, ERP sistemleri, muhasebe yazılımları ve kargo şirketleri arasında tam otomasyon sağlar.

### Temel Farklar

| Rakip | Eksiklik | INT Çözümü |
|-------|----------|------------|
| Stockmount | Güvenilirlik sorunları, 8+ gün sync hataları | Event-driven architecture, 99.9% SLA |
| Sopyo | Basic AI, enterprise features yok | Multi-LLM AI core, SOC 2 compliance |
| Entegra | Yüksek fiyat, sınırlı otomasyon | Transparent pricing, visual workflow builder |
| Zapier/Make | Türkiye pazaryerleri yok | Native Trendyol/HB/N11 desteği |

---

## 1. Competitive Feature Matrix

### 1.1 Türkiye Pazaryeri Entegratörleri

| Özellik | Stockmount | Sopyo | Yengeç | Entegra | **INT** |
|---------|------------|-------|--------|---------|---------|
| **Pazaryerleri** | 8+ | 10+ | 6+ | 10+ | **15+** |
| **E-ticaret Altyapıları** | 5 | 10+ | 4 | 8 | **20+** |
| **ERP Entegrasyonları** | 5 | 14+ | 3 | 10 | **25+** |
| **AI Ürün Eşleştirme** | ❌ | Basic | ❌ | ❌ | **Multi-modal ML** |
| **AI Fiyatlama** | ❌ | 100 robot | ❌ | ❌ | **Reinforcement Learning** |
| **Natural Language Config** | ❌ | ❌ | ❌ | ❌ | **✅** |
| **Visual Workflow Builder** | ❌ | ❌ | ❌ | ❌ | **✅** |
| **SOC 2 Type II** | ❌ | ❌ | ❌ | ❌ | **✅** |
| **RBAC + SSO** | Basic | Limited | ❌ | Basic | **Full** |
| **SLA Guarantee** | ❌ | ❌ | ❌ | ❌ | **99.9%** |
| **Multi-warehouse Routing** | Limited | Basic | ❌ | Basic | **AI-optimized** |
| **API-first** | Basic | v2 | ❌ | Basic | **Full REST + GraphQL** |
| **Webhook Support** | ❌ | Limited | ❌ | ❌ | **Full bi-directional** |
| **Real-time Sync** | 15-30 min | 5-15 min | 30 min | 15 min | **<1 min** |
| **White-label** | ❌ | ❌ | ❌ | ❌ | **✅** |

### 1.2 Global iPaaS Karşılaştırması

| Özellik | Zapier | Make | n8n | Workato | **INT** |
|---------|--------|------|-----|---------|---------|
| **Türkiye Pazaryerleri** | ❌ | ❌ | ❌ | ❌ | **Native** |
| **E-ticaret Focus** | Generic | Generic | Generic | Generic | **Specialized** |
| **Self-hosted Option** | ❌ | ❌ | ✅ | ❌ | **✅** |
| **Frappe/ERPNext Native** | ❌ | ❌ | ❌ | ❌ | **✅** |
| **Multi-LLM Support** | ❌ | Limited | ❌ | GPT only | **OpenAI+Gemini+Claude** |
| **PIM Integration** | ❌ | ❌ | ❌ | ❌ | **Native** |
| **Turkish Support** | ❌ | ❌ | ❌ | ❌ | **Full** |
| **KVKK Compliance** | ❌ | ❌ | ❌ | ❌ | **✅** |

---

## 2. Technical Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           INT Platform                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Web UI    │  │  Mobile UI  │  │   REST API  │  │ GraphQL API │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         └────────────────┴────────────────┴────────────────┘           │
│                                    │                                    │
│  ┌─────────────────────────────────┴─────────────────────────────────┐ │
│  │                    Frappe Framework Core                          │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ │ │
│  │  │ DocTypes │ │   Auth   │ │  Perms   │ │ Workflow │ │  Cache  │ │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └─────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                    │                                    │
│  ┌────────────────────────────────┴────────────────────────────────┐  │
│  │                        INT Core Modules                          │  │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ │  │
│  │ │Connector │ │ Workflow │ │   EDA    │ │AI Engine │ │Analytics│ │  │
│  │ │ Manager  │ │  Engine  │ │  Core    │ │  (Multi) │ │  Engine │ │  │
│  │ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └─────────┘ │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│  ┌────────────────────────────────┴────────────────────────────────┐  │
│  │                    Integration Layer                             │  │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ │  │
│  │ │Trendyol  │ │Hepsiburada│ │  Amazon  │ │   n11   │ │ 50+ more│ │  │
│  │ │Connector │ │ Connector │ │Connector │ │Connector│ │connectors│ │  │
│  │ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └─────────┘ │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐         ┌─────────────────┐         ┌───────────────┐
│  Marketplaces │         │   ERP Systems   │         │   Services    │
│  - Trendyol   │         │   - ERPNext     │         │   - Kargo     │
│  - Hepsiburada│         │   - Logo        │         │   - E-fatura  │
│  - Amazon TR  │         │   - Netsis      │         │   - SMS/Email │
│  - n11        │         │   - SAP B1      │         │   - Webhook   │
│  - 50+ more   │         │   - 20+ more    │         │   - 30+ more  │
└───────────────┘         └─────────────────┘         └───────────────┘
```

### 2.2 Event-Driven Architecture (EDA)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Event Bus (Redis Streams)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│   │ order.*  │    │product.* │    │ stock.*  │    │ price.*  │     │
│   └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘     │
│        │               │               │               │            │
│   ┌────┴────┐     ┌────┴────┐     ┌────┴────┐     ┌────┴────┐      │
│   │Consumer │     │Consumer │     │Consumer │     │Consumer │      │
│   │ Group 1 │     │ Group 2 │     │ Group 3 │     │ Group 4 │      │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌───────────┐       ┌───────────┐       ┌───────────┐
    │  Handler  │       │  Handler  │       │  Handler  │
    │  Workers  │       │ AI Agent  │       │  Webhook  │
    │  (Frappe) │       │  (CrewAI) │       │ Dispatcher│
    └───────────┘       └───────────┘       └───────────┘
```

### 2.3 AI Architecture - Multi-LLM Support

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI Orchestration Layer                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    INT AI Router                             │    │
│  │  - Model Selection Logic                                     │    │
│  │  - Cost Optimization                                         │    │
│  │  - Fallback Handling                                         │    │
│  │  - Response Caching                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│         ┌────────────────────┼────────────────────┐                 │
│         ▼                    ▼                    ▼                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐         │
│  │   OpenAI    │      │   Gemini    │      │   Claude    │         │
│  │  Connector  │      │  Connector  │      │  Connector  │         │
│  │             │      │             │      │             │         │
│  │ - GPT-4o    │      │ - 2.0 Flash │      │ - Sonnet    │         │
│  │ - GPT-4o-m  │      │ - 2.0 Pro   │      │ - Opus      │         │
│  │ - o1        │      │ - 1.5 Pro   │      │ - Haiku     │         │
│  └─────────────┘      └─────────────┘      └─────────────┘         │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    CrewAI Integration                        │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │    │
│  │  │ Product │  │ Pricing │  │ Support │  │ Analyst │        │    │
│  │  │ Matcher │  │ Agent   │  │ Agent   │  │ Agent   │        │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    MCP (Model Context Protocol)              │    │
│  │  - Frappe DocType Access                                     │    │
│  │  - External Tool Integration                                 │    │
│  │  - Standardized Context Passing                              │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. DocType Specifications

### 3.1 Core DocTypes

#### 3.1.1 INT Settings (Singleton)

```python
# int/int/doctype/int_settings/int_settings.py

class INTSettings(Document):
    """
    Global settings for INT platform
    
    Fields:
    - company: Link to Company
    - default_warehouse: Link to Warehouse
    - sync_interval_minutes: Int (default: 5)
    - enable_ai_features: Check
    - default_ai_provider: Select [OpenAI, Gemini, Claude]
    - openai_api_key: Password
    - gemini_api_key: Password
    - anthropic_api_key: Password
    - enable_webhook_signing: Check
    - webhook_secret: Password
    - max_retry_attempts: Int (default: 3)
    - retry_backoff_multiplier: Float (default: 2.0)
    - enable_dead_letter_queue: Check
    - log_retention_days: Int (default: 90)
    - enable_audit_logging: Check
    """
```

#### 3.1.2 INT Connector

```python
# int/int/doctype/int_connector/int_connector.py

class INTConnector(Document):
    """
    Marketplace/Service connector configuration
    
    Fields:
    - connector_name: Data (required)
    - connector_type: Select [Marketplace, ECommerce, ERP, Accounting, Cargo, Payment, Other]
    - platform: Link to INT Platform
    - enabled: Check
    - credentials: Table (INT Connector Credential)
    - base_url: Data
    - sandbox_url: Data
    - use_sandbox: Check
    - rate_limit_per_minute: Int
    - rate_limit_per_day: Int
    - webhook_url: Data (read-only, auto-generated)
    - webhook_secret: Password
    - last_sync_at: Datetime
    - sync_status: Select [Idle, Syncing, Error, Paused]
    - error_message: Long Text
    - sync_products: Check
    - sync_orders: Check
    - sync_inventory: Check
    - sync_prices: Check
    - sync_interval_override: Int (minutes)
    - field_mappings: Table (INT Field Mapping)
    - transform_rules: Table (INT Transform Rule)
    """
    
    def before_insert(self):
        self.webhook_url = self.generate_webhook_url()
        self.webhook_secret = frappe.generate_hash(length=32)
    
    def generate_webhook_url(self):
        site_url = frappe.utils.get_url()
        return f"{site_url}/api/method/int.api.webhook.handle/{self.name}"
```

#### 3.1.3 INT Platform (Master Data)

```python
# int/int/doctype/int_platform/int_platform.py

class INTPlatform(Document):
    """
    Platform definitions (Trendyol, Hepsiburada, etc.)
    
    Fields:
    - platform_name: Data (required)
    - platform_code: Data (unique, required)
    - platform_type: Select [Marketplace, ECommerce, ERP, Accounting, Cargo, Payment]
    - logo: Attach Image
    - documentation_url: Data
    - api_version: Data
    - auth_type: Select [API_Key, OAuth2, Basic, Bearer, Custom]
    - oauth_authorize_url: Data
    - oauth_token_url: Data
    - oauth_scopes: Small Text
    - rate_limits: Table (INT Rate Limit)
    - supported_operations: Table (INT Platform Operation)
    - field_schema: JSON (platform-specific field definitions)
    - category_mapping_required: Check
    - attribute_mapping_required: Check
    - sandbox_available: Check
    - webhook_supported: Check
    - webhook_events: Table (INT Webhook Event Type)
    """
```

#### 3.1.4 INT Event

```python
# int/int/doctype/int_event/int_event.py

class INTEvent(Document):
    """
    Event sourcing - all state changes as immutable events
    
    Fields:
    - event_id: Data (auto-generated UUID)
    - event_type: Select [order.created, order.updated, order.cancelled,
                          product.created, product.updated, product.deleted,
                          inventory.updated, price.updated, 
                          shipment.created, shipment.updated,
                          return.requested, return.approved, return.completed]
    - connector: Link to INT Connector
    - source: Select [Marketplace, ERP, Manual, API, Webhook, Scheduler]
    - payload: JSON
    - payload_hash: Data (for deduplication)
    - correlation_id: Data (for tracing related events)
    - causation_id: Data (which event caused this)
    - processed: Check
    - processed_at: Datetime
    - processing_attempts: Int
    - last_error: Long Text
    - dead_letter: Check
    - idempotency_key: Data (unique)
    """
    
    def before_insert(self):
        import hashlib
        import json
        
        self.event_id = frappe.generate_hash(length=32)
        self.payload_hash = hashlib.sha256(
            json.dumps(self.payload, sort_keys=True).encode()
        ).hexdigest()
        self.idempotency_key = f"{self.connector}:{self.event_type}:{self.payload_hash}"
```

#### 3.1.5 INT Workflow

```python
# int/int/doctype/int_workflow/int_workflow.py

class INTWorkflow(Document):
    """
    Visual workflow builder - Zapier/Make style
    
    Fields:
    - workflow_name: Data (required)
    - description: Small Text
    - enabled: Check
    - trigger_type: Select [Event, Schedule, Manual, Webhook]
    - trigger_config: JSON
    - nodes: Table (INT Workflow Node)
    - connections: Table (INT Workflow Connection)
    - variables: Table (INT Workflow Variable)
    - error_handling: Select [Stop, Continue, Retry, Notify]
    - max_execution_time: Int (seconds)
    - execution_count: Int (read-only)
    - last_executed_at: Datetime
    - last_execution_status: Select [Success, Failed, Timeout]
    - version: Int
    - published_version: Int
    - canvas_data: JSON (for visual editor state)
    """
```

#### 3.1.6 INT Workflow Node

```python
# int/int/doctype/int_workflow_node/int_workflow_node.py

class INTWorkflowNode(Document):
    """
    Individual node in a workflow
    
    Fields:
    - node_id: Data (auto-generated)
    - node_type: Select [Trigger, Action, Condition, Loop, Delay, 
                         AI_Process, Transform, HTTP_Request, 
                         Send_Email, Send_SMS, Webhook, Code]
    - node_name: Data
    - connector: Link to INT Connector (optional)
    - operation: Data (connector-specific operation)
    - config: JSON
    - input_mapping: JSON
    - output_mapping: JSON
    - condition_expression: Code (for Condition nodes)
    - retry_config: JSON
    - timeout_seconds: Int
    - position_x: Int (canvas position)
    - position_y: Int (canvas position)
    """
```

#### 3.1.7 INT AI Agent

```python
# int/int/doctype/int_ai_agent/int_ai_agent.py

class INTAIAgent(Document):
    """
    AI Agent definition (CrewAI compatible)
    
    Fields:
    - agent_name: Data (required)
    - agent_type: Select [Product_Matcher, Price_Optimizer, 
                          Category_Mapper, Content_Generator,
                          Demand_Forecaster, Anomaly_Detector,
                          Support_Agent, Custom]
    - description: Small Text
    - role: Small Text (CrewAI role)
    - goal: Small Text (CrewAI goal)
    - backstory: Text (CrewAI backstory)
    - llm_provider: Select [OpenAI, Gemini, Claude]
    - llm_model: Data
    - temperature: Float (0.0 - 2.0)
    - max_tokens: Int
    - tools: Table (INT AI Tool)
    - memory_enabled: Check
    - verbose: Check
    - allow_delegation: Check
    - max_iterations: Int
    - system_prompt: Text
    - few_shot_examples: Table (INT AI Example)
    """
```

#### 3.1.8 INT Sync Log

```python
# int/int/doctype/int_sync_log/int_sync_log.py

class INTSyncLog(Document):
    """
    Detailed sync operation logging
    
    Fields:
    - log_id: Data (auto-generated)
    - connector: Link to INT Connector
    - operation: Select [Product_Sync, Order_Sync, Inventory_Sync, 
                         Price_Sync, Category_Sync, Full_Sync]
    - direction: Select [Inbound, Outbound, Bidirectional]
    - started_at: Datetime
    - completed_at: Datetime
    - duration_seconds: Float
    - status: Select [Running, Completed, Failed, Partial]
    - records_processed: Int
    - records_created: Int
    - records_updated: Int
    - records_failed: Int
    - records_skipped: Int
    - error_details: Table (INT Sync Error)
    - request_payload: JSON (for debugging)
    - response_payload: JSON (for debugging)
    - triggered_by: Link to User
    - trigger_source: Select [Manual, Scheduler, Webhook, API, Event]
    """
```

#### 3.1.9 INT Product Mapping

```python
# int/int/doctype/int_product_mapping/int_product_mapping.py

class INTProductMapping(Document):
    """
    Maps PIM products to marketplace products
    
    Fields:
    - pim_product: Link to PIM Product (from PIM app)
    - connector: Link to INT Connector
    - marketplace_product_id: Data
    - marketplace_sku: Data
    - marketplace_barcode: Data
    - marketplace_url: Data
    - listing_status: Select [Active, Inactive, Pending, Rejected, Draft]
    - listing_errors: Table (INT Listing Error)
    - category_mapping: Link to INT Category Mapping
    - attribute_mappings: Table (INT Attribute Mapping)
    - price_override: Currency
    - stock_override: Int
    - sync_enabled: Check
    - last_synced_at: Datetime
    - match_confidence: Percent (AI-generated)
    - match_method: Select [Manual, Barcode, SKU, AI_Matched, Title_Match]
    - marketplace_data: JSON (raw marketplace response)
    """
```

#### 3.1.10 INT Order

```python
# int/int/doctype/int_order/int_order.py

class INTOrder(Document):
    """
    Marketplace orders (linked to ERPNext Sales Order)
    
    Fields:
    - order_id: Data (marketplace order ID)
    - connector: Link to INT Connector
    - sales_order: Link to Sales Order (ERPNext)
    - marketplace_status: Data
    - int_status: Select [New, Processing, Shipped, Delivered, 
                          Cancelled, Returned, Refunded]
    - order_date: Datetime
    - customer_name: Data
    - customer_email: Data
    - customer_phone: Data
    - shipping_address: Text
    - billing_address: Text
    - items: Table (INT Order Item)
    - subtotal: Currency
    - shipping_cost: Currency
    - discount_amount: Currency
    - tax_amount: Currency
    - total_amount: Currency
    - currency: Link to Currency
    - payment_method: Data
    - payment_status: Select [Pending, Paid, Refunded, Partial]
    - shipment_packages: Table (INT Shipment Package)
    - notes: Text
    - raw_data: JSON
    - invoice_url: Data
    - invoice_number: Data
    - tracking_numbers: Small Text
    - estimated_delivery: Date
    - delivered_at: Datetime
    """
```

### 3.2 AI-Specific DocTypes

#### 3.2.1 INT AI Task

```python
# int/int/doctype/int_ai_task/int_ai_task.py

class INTAITask(Document):
    """
    AI task execution tracking
    
    Fields:
    - task_id: Data (auto-generated)
    - task_type: Select [Product_Matching, Category_Mapping, 
                         Price_Optimization, Content_Generation,
                         Demand_Forecast, Anomaly_Detection,
                         Natural_Language_Query, Custom]
    - agent: Link to INT AI Agent
    - input_data: JSON
    - output_data: JSON
    - prompt_used: Long Text
    - model_used: Data
    - tokens_input: Int
    - tokens_output: Int
    - cost_usd: Float
    - started_at: Datetime
    - completed_at: Datetime
    - duration_ms: Int
    - status: Select [Pending, Running, Completed, Failed, Timeout]
    - error_message: Long Text
    - confidence_score: Percent
    - human_review_required: Check
    - human_review_status: Select [Pending, Approved, Rejected, Modified]
    - reviewed_by: Link to User
    - reviewed_at: Datetime
    - feedback: Text
    """
```

#### 3.2.2 INT AI Crew

```python
# int/int/doctype/int_ai_crew/int_ai_crew.py

class INTAICrew(Document):
    """
    CrewAI crew definition
    
    Fields:
    - crew_name: Data (required)
    - description: Small Text
    - agents: Table (INT AI Crew Agent)
    - tasks: Table (INT AI Crew Task)
    - process: Select [Sequential, Hierarchical]
    - manager_agent: Link to INT AI Agent (for hierarchical)
    - verbose: Check
    - memory: Check
    - cache: Check
    - max_rpm: Int (rate limit)
    - share_crew: Check
    """
```

---

## 4. Connector Implementation Guide

### 4.1 Base Connector Class

```python
# int/int/connectors/base.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import frappe
from frappe.utils import now_datetime
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class SyncResult:
    success: bool
    records_processed: int
    records_created: int
    records_updated: int
    records_failed: int
    errors: List[Dict]
    data: Optional[Any] = None


class BaseConnector(ABC):
    """
    Abstract base class for all connectors
    """
    
    def __init__(self, connector_doc: str):
        self.connector = frappe.get_doc("INT Connector", connector_doc)
        self.platform = frappe.get_doc("INT Platform", self.connector.platform)
        self._session = None
        self._rate_limiter = None
    
    @property
    def session(self) -> requests.Session:
        if not self._session:
            self._session = requests.Session()
            self._setup_auth()
        return self._session
    
    @abstractmethod
    def _setup_auth(self):
        """Configure authentication for the session"""
        pass
    
    @property
    def base_url(self) -> str:
        if self.connector.use_sandbox:
            return self.connector.sandbox_url or self.platform.sandbox_url
        return self.connector.base_url or self.platform.base_url
    
    # ==================== PRODUCT OPERATIONS ====================
    
    @abstractmethod
    def get_products(self, page: int = 1, page_size: int = 100, 
                     filters: Optional[Dict] = None) -> List[Dict]:
        """Fetch products from marketplace"""
        pass
    
    @abstractmethod
    def create_product(self, product_data: Dict) -> Dict:
        """Create a new product listing"""
        pass
    
    @abstractmethod
    def update_product(self, marketplace_id: str, product_data: Dict) -> Dict:
        """Update an existing product listing"""
        pass
    
    @abstractmethod
    def delete_product(self, marketplace_id: str) -> bool:
        """Delete/deactivate a product listing"""
        pass
    
    # ==================== INVENTORY OPERATIONS ====================
    
    @abstractmethod
    def update_inventory(self, updates: List[Dict]) -> SyncResult:
        """
        Batch update inventory
        updates: [{"sku": "XXX", "quantity": 10}, ...]
        """
        pass
    
    @abstractmethod
    def get_inventory(self, skus: Optional[List[str]] = None) -> List[Dict]:
        """Get current inventory levels"""
        pass
    
    # ==================== PRICE OPERATIONS ====================
    
    @abstractmethod
    def update_prices(self, updates: List[Dict]) -> SyncResult:
        """
        Batch update prices
        updates: [{"sku": "XXX", "price": 99.99, "sale_price": 79.99}, ...]
        """
        pass
    
    # ==================== ORDER OPERATIONS ====================
    
    @abstractmethod
    def get_orders(self, status: Optional[str] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None,
                   page: int = 1, page_size: int = 100) -> List[Dict]:
        """Fetch orders from marketplace"""
        pass
    
    @abstractmethod
    def update_order_status(self, order_id: str, status: str, 
                            tracking_info: Optional[Dict] = None) -> Dict:
        """Update order status (ship, deliver, cancel)"""
        pass
    
    @abstractmethod
    def create_shipment(self, order_id: str, shipment_data: Dict) -> Dict:
        """Create shipment for an order"""
        pass
    
    # ==================== CATEGORY OPERATIONS ====================
    
    @abstractmethod
    def get_categories(self) -> List[Dict]:
        """Fetch category tree from marketplace"""
        pass
    
    @abstractmethod
    def get_category_attributes(self, category_id: str) -> List[Dict]:
        """Get required/optional attributes for a category"""
        pass
    
    # ==================== WEBHOOK HANDLING ====================
    
    def handle_webhook(self, payload: Dict, headers: Dict) -> Dict:
        """Process incoming webhook"""
        # Verify signature
        if self.connector.webhook_secret:
            if not self._verify_webhook_signature(payload, headers):
                frappe.throw("Invalid webhook signature")
        
        # Parse event type
        event_type = self._parse_webhook_event_type(payload)
        
        # Create event record
        event = frappe.get_doc({
            "doctype": "INT Event",
            "event_type": event_type,
            "connector": self.connector.name,
            "source": "Webhook",
            "payload": payload
        })
        event.insert(ignore_permissions=True)
        
        return {"status": "received", "event_id": event.event_id}
    
    @abstractmethod
    def _verify_webhook_signature(self, payload: Dict, headers: Dict) -> bool:
        """Verify webhook signature"""
        pass
    
    @abstractmethod
    def _parse_webhook_event_type(self, payload: Dict) -> str:
        """Extract event type from webhook payload"""
        pass
    
    # ==================== HELPER METHODS ====================
    
    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, min=4, max=60))
    def _make_request(self, method: str, endpoint: str, 
                      data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> requests.Response:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=30
        )
        
        # Log the request
        self._log_request(method, url, data, response)
        
        response.raise_for_status()
        return response
    
    def _log_request(self, method: str, url: str, 
                     data: Optional[Dict], response: requests.Response):
        """Log API request for debugging"""
        frappe.get_doc({
            "doctype": "INT API Log",
            "connector": self.connector.name,
            "method": method,
            "url": url,
            "request_data": frappe.as_json(data) if data else None,
            "response_status": response.status_code,
            "response_data": response.text[:10000],  # Truncate
            "timestamp": now_datetime()
        }).insert(ignore_permissions=True)
    
    def _transform_to_marketplace(self, data: Dict, mapping_type: str) -> Dict:
        """Transform data from internal format to marketplace format"""
        field_mappings = self.connector.field_mappings
        result = {}
        
        for mapping in field_mappings:
            if mapping.mapping_type != mapping_type:
                continue
            
            source_value = self._get_nested_value(data, mapping.source_field)
            
            if mapping.transform_function:
                source_value = self._apply_transform(
                    source_value, 
                    mapping.transform_function
                )
            
            if source_value is None and mapping.default_value:
                source_value = mapping.default_value
            
            if source_value is not None or mapping.include_null:
                self._set_nested_value(result, mapping.target_field, source_value)
        
        return result
    
    def _transform_from_marketplace(self, data: Dict, mapping_type: str) -> Dict:
        """Transform data from marketplace format to internal format"""
        # Reverse of _transform_to_marketplace
        pass
```

### 4.2 Trendyol Connector Implementation

```python
# int/int/connectors/trendyol.py

import base64
from typing import Dict, List, Optional
from .base import BaseConnector, SyncResult


class TrendyolConnector(BaseConnector):
    """
    Trendyol Marketplace Connector
    API Docs: https://developers.trendyol.com
    """
    
    def _setup_auth(self):
        """Setup Basic Auth for Trendyol"""
        credentials = {c.credential_key: c.credential_value 
                       for c in self.connector.credentials}
        
        api_key = credentials.get("api_key")
        api_secret = credentials.get("api_secret")
        
        if not api_key or not api_secret:
            frappe.throw("Trendyol API key and secret are required")
        
        auth_string = base64.b64encode(
            f"{api_key}:{api_secret}".encode()
        ).decode()
        
        self.session.headers.update({
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/json",
            "User-Agent": f"INT-Platform/{frappe.get_module('int').__version__}"
        })
        
        self.supplier_id = credentials.get("supplier_id")
    
    # ==================== PRODUCT OPERATIONS ====================
    
    def get_products(self, page: int = 0, page_size: int = 100,
                     filters: Optional[Dict] = None) -> List[Dict]:
        """
        Fetch products from Trendyol
        GET /sapigw/suppliers/{supplierId}/products
        """
        params = {
            "page": page,
            "size": min(page_size, 100),  # Max 100
            "approved": True
        }
        
        if filters:
            if filters.get("barcode"):
                params["barcode"] = filters["barcode"]
            if filters.get("sku"):
                params["stockCode"] = filters["sku"]
        
        response = self._make_request(
            "GET",
            f"sapigw/suppliers/{self.supplier_id}/products",
            params=params
        )
        
        data = response.json()
        return [self._transform_from_marketplace(p, "product") 
                for p in data.get("content", [])]
    
    def create_product(self, product_data: Dict) -> Dict:
        """
        Create product on Trendyol
        POST /sapigw/suppliers/{supplierId}/v2/products
        """
        # Transform to Trendyol format
        trendyol_data = self._transform_to_marketplace(product_data, "product")
        
        # Required fields validation
        required_fields = ["barcode", "title", "productMainId", 
                          "brandId", "categoryId", "quantity",
                          "stockCode", "dimensionalWeight",
                          "description", "currencyType",
                          "listPrice", "salePrice", "vatRate",
                          "cargoCompanyId", "shipmentAddressId",
                          "returningAddressId", "images"]
        
        for field in required_fields:
            if field not in trendyol_data:
                frappe.throw(f"Required field missing: {field}")
        
        payload = {"items": [trendyol_data]}
        
        response = self._make_request(
            "POST",
            f"sapigw/suppliers/{self.supplier_id}/v2/products",
            data=payload
        )
        
        result = response.json()
        return {
            "batch_request_id": result.get("batchRequestId"),
            "status": "pending"
        }
    
    def update_product(self, marketplace_id: str, product_data: Dict) -> Dict:
        """
        Update product on Trendyol
        PUT /sapigw/suppliers/{supplierId}/v2/products
        """
        trendyol_data = self._transform_to_marketplace(product_data, "product")
        trendyol_data["barcode"] = marketplace_id
        
        payload = {"items": [trendyol_data]}
        
        response = self._make_request(
            "PUT",
            f"sapigw/suppliers/{self.supplier_id}/v2/products",
            data=payload
        )
        
        return response.json()
    
    def delete_product(self, marketplace_id: str) -> bool:
        """
        Delete/deactivate product on Trendyol
        DELETE /sapigw/suppliers/{supplierId}/v2/products
        """
        payload = {"items": [{"barcode": marketplace_id}]}
        
        response = self._make_request(
            "DELETE",
            f"sapigw/suppliers/{self.supplier_id}/v2/products",
            data=payload
        )
        
        return response.status_code == 200
    
    # ==================== INVENTORY OPERATIONS ====================
    
    def update_inventory(self, updates: List[Dict]) -> SyncResult:
        """
        Batch update stock on Trendyol
        POST /sapigw/suppliers/{supplierId}/products/price-and-inventory
        """
        items = []
        for update in updates:
            items.append({
                "barcode": update["barcode"],
                "quantity": update["quantity"],
                "salePrice": update.get("price"),
                "listPrice": update.get("list_price")
            })
        
        # Trendyol allows max 100 items per request
        results = SyncResult(
            success=True, records_processed=0, records_created=0,
            records_updated=0, records_failed=0, errors=[]
        )
        
        for i in range(0, len(items), 100):
            batch = items[i:i+100]
            
            try:
                response = self._make_request(
                    "POST",
                    f"sapigw/suppliers/{self.supplier_id}/products/price-and-inventory",
                    data={"items": batch}
                )
                
                result = response.json()
                results.records_processed += len(batch)
                results.records_updated += len(batch)
                
            except Exception as e:
                results.records_failed += len(batch)
                results.errors.append({
                    "batch_start": i,
                    "error": str(e)
                })
        
        return results
    
    def get_inventory(self, skus: Optional[List[str]] = None) -> List[Dict]:
        """Get inventory from Trendyol products"""
        products = self.get_products()
        return [{"sku": p["stockCode"], "quantity": p["quantity"]} 
                for p in products]
    
    # ==================== ORDER OPERATIONS ====================
    
    def get_orders(self, status: Optional[str] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None,
                   page: int = 0, page_size: int = 100) -> List[Dict]:
        """
        Fetch orders from Trendyol
        GET /sapigw/suppliers/{supplierId}/orders
        """
        params = {
            "page": page,
            "size": min(page_size, 200)  # Max 200
        }
        
        if status:
            status_map = {
                "new": "Created",
                "processing": "Picking",
                "shipped": "Shipped",
                "delivered": "Delivered",
                "cancelled": "Cancelled"
            }
            params["status"] = status_map.get(status, status)
        
        if start_date:
            params["startDate"] = self._to_timestamp(start_date)
        if end_date:
            params["endDate"] = self._to_timestamp(end_date)
        
        response = self._make_request(
            "GET",
            f"sapigw/suppliers/{self.supplier_id}/orders",
            params=params
        )
        
        data = response.json()
        return [self._transform_order(o) for o in data.get("content", [])]
    
    def update_order_status(self, order_id: str, status: str,
                            tracking_info: Optional[Dict] = None) -> Dict:
        """
        Update order status on Trendyol
        """
        if status == "shipped":
            return self.create_shipment(order_id, tracking_info or {})
        elif status == "cancelled":
            return self._cancel_order(order_id)
        
        frappe.throw(f"Unsupported status update: {status}")
    
    def create_shipment(self, order_id: str, shipment_data: Dict) -> Dict:
        """
        Create shipment package
        PUT /sapigw/suppliers/{supplierId}/{shipmentPackageId}
        """
        package_id = shipment_data.get("package_id", order_id)
        tracking_number = shipment_data.get("tracking_number")
        
        payload = {
            "lines": shipment_data.get("lines", []),
            "params": {}
        }
        
        if tracking_number:
            payload["params"]["invoiceLink"] = shipment_data.get("invoice_link", "")
        
        response = self._make_request(
            "PUT",
            f"sapigw/suppliers/{self.supplier_id}/{package_id}",
            data=payload
        )
        
        return response.json()
    
    # ==================== CATEGORY OPERATIONS ====================
    
    def get_categories(self) -> List[Dict]:
        """
        Get Trendyol category tree
        GET /sapigw/product-categories
        """
        response = self._make_request("GET", "sapigw/product-categories")
        
        categories = response.json().get("categories", [])
        return self._flatten_categories(categories)
    
    def get_category_attributes(self, category_id: str) -> List[Dict]:
        """
        Get category attributes
        GET /sapigw/product-categories/{categoryId}/attributes
        """
        response = self._make_request(
            "GET",
            f"sapigw/product-categories/{category_id}/attributes"
        )
        
        data = response.json()
        return data.get("categoryAttributes", [])
    
    # ==================== HELPER METHODS ====================
    
    def _transform_order(self, order_data: Dict) -> Dict:
        """Transform Trendyol order to internal format"""
        return {
            "order_id": str(order_data.get("orderNumber")),
            "marketplace_status": order_data.get("status"),
            "order_date": self._from_timestamp(order_data.get("orderDate")),
            "customer_name": f"{order_data.get('customerFirstName', '')} {order_data.get('customerLastName', '')}".strip(),
            "customer_email": order_data.get("customerEmail"),
            "shipping_address": self._format_address(order_data.get("shipmentAddress", {})),
            "billing_address": self._format_address(order_data.get("invoiceAddress", {})),
            "items": [
                {
                    "sku": line.get("merchantSku"),
                    "barcode": line.get("barcode"),
                    "product_name": line.get("productName"),
                    "quantity": line.get("quantity"),
                    "unit_price": line.get("price"),
                    "discount": line.get("discount", 0),
                    "tax": line.get("vatBaseAmount", 0)
                }
                for line in order_data.get("lines", [])
            ],
            "total_amount": order_data.get("totalPrice"),
            "currency": order_data.get("currencyCode", "TRY"),
            "raw_data": order_data
        }
    
    def _verify_webhook_signature(self, payload: Dict, headers: Dict) -> bool:
        """Verify Trendyol webhook signature"""
        # Trendyol uses IP whitelist, not signature
        # Implement IP check if needed
        return True
    
    def _parse_webhook_event_type(self, payload: Dict) -> str:
        """Parse Trendyol webhook event type"""
        event_type = payload.get("eventType", "")
        
        event_map = {
            "OrderCreated": "order.created",
            "OrderCancelled": "order.cancelled",
            "OrderShipped": "shipment.created",
            "OrderDelivered": "shipment.updated",
            "ReturnCreated": "return.requested"
        }
        
        return event_map.get(event_type, f"unknown.{event_type}")
    
    def _to_timestamp(self, date_str: str) -> int:
        """Convert date string to millisecond timestamp"""
        from datetime import datetime
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)
    
    def _from_timestamp(self, ts: int) -> str:
        """Convert millisecond timestamp to ISO date string"""
        from datetime import datetime
        return datetime.fromtimestamp(ts / 1000).isoformat()
    
    def _format_address(self, addr: Dict) -> str:
        """Format address dict to string"""
        parts = [
            addr.get("fullAddress", ""),
            addr.get("district", ""),
            addr.get("city", ""),
            addr.get("country", "")
        ]
        return ", ".join(p for p in parts if p)
    
    def _flatten_categories(self, categories: List[Dict], 
                            parent_path: str = "") -> List[Dict]:
        """Flatten category tree"""
        result = []
        for cat in categories:
            path = f"{parent_path}/{cat['name']}" if parent_path else cat['name']
            result.append({
                "id": cat["id"],
                "name": cat["name"],
                "path": path,
                "parent_id": cat.get("parentId")
            })
            if cat.get("subCategories"):
                result.extend(self._flatten_categories(cat["subCategories"], path))
        return result


# Connector registry
CONNECTOR_REGISTRY = {
    "trendyol": TrendyolConnector,
    "hepsiburada": "int.connectors.hepsiburada.HepsiburadaConnector",
    "amazon_tr": "int.connectors.amazon.AmazonTRConnector",
    "n11": "int.connectors.n11.N11Connector",
    # ... more connectors
}
```

---

## 5. AI Engine Implementation

### 5.1 Multi-LLM Router

```python
# int/int/ai/router.py

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import frappe


class LLMProvider(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"


@dataclass
class LLMConfig:
    provider: LLMProvider
    model: str
    api_key: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    tokens_input: int
    tokens_output: int
    cost_usd: float
    latency_ms: int
    raw_response: Dict


class INTAIRouter:
    """
    Intelligent LLM routing with fallback and cost optimization
    """
    
    # Cost per 1M tokens (approximate, update as needed)
    PRICING = {
        "openai": {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "o1": {"input": 15.00, "output": 60.00},
            "o1-mini": {"input": 3.00, "output": 12.00}
        },
        "gemini": {
            "gemini-2.0-flash": {"input": 0.075, "output": 0.30},
            "gemini-2.0-pro": {"input": 1.25, "output": 5.00},
            "gemini-1.5-pro": {"input": 1.25, "output": 5.00}
        },
        "claude": {
            "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
            "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
            "claude-haiku-4-20250514": {"input": 0.25, "output": 1.25}
        }
    }
    
    # Task-to-model recommendations
    TASK_ROUTING = {
        "product_matching": {
            "primary": ("gemini", "gemini-2.0-flash"),  # Fast, good at structured data
            "fallback": ("openai", "gpt-4o-mini")
        },
        "content_generation": {
            "primary": ("claude", "claude-sonnet-4-20250514"),  # Best writing
            "fallback": ("openai", "gpt-4o")
        },
        "category_mapping": {
            "primary": ("gemini", "gemini-2.0-flash"),
            "fallback": ("openai", "gpt-4o-mini")
        },
        "demand_forecast": {
            "primary": ("openai", "o1-mini"),  # Best reasoning
            "fallback": ("claude", "claude-sonnet-4-20250514")
        },
        "anomaly_detection": {
            "primary": ("openai", "gpt-4o"),
            "fallback": ("gemini", "gemini-2.0-pro")
        },
        "natural_language_query": {
            "primary": ("claude", "claude-sonnet-4-20250514"),
            "fallback": ("openai", "gpt-4o")
        }
    }
    
    def __init__(self):
        self.settings = frappe.get_single("INT Settings")
        self._clients = {}
    
    def get_client(self, provider: LLMProvider):
        """Get or create LLM client"""
        if provider.value not in self._clients:
            self._clients[provider.value] = self._create_client(provider)
        return self._clients[provider.value]
    
    def _create_client(self, provider: LLMProvider):
        """Create LLM client based on provider"""
        if provider == LLMProvider.OPENAI:
            from openai import OpenAI
            return OpenAI(api_key=self.settings.openai_api_key)
        
        elif provider == LLMProvider.GEMINI:
            import google.generativeai as genai
            genai.configure(api_key=self.settings.gemini_api_key)
            return genai
        
        elif provider == LLMProvider.CLAUDE:
            from anthropic import Anthropic
            return Anthropic(api_key=self.settings.anthropic_api_key)
    
    def complete(self, 
                 prompt: str,
                 task_type: str = "general",
                 system_prompt: Optional[str] = None,
                 provider: Optional[str] = None,
                 model: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 4096,
                 json_mode: bool = False,
                 retry_on_failure: bool = True) -> LLMResponse:
        """
        Complete a prompt with intelligent routing
        """
        import time
        
        # Determine provider/model
        if not provider or not model:
            routing = self.TASK_ROUTING.get(task_type, {})
            provider, model = routing.get("primary", 
                                          (self.settings.default_ai_provider.lower(), 
                                           "gpt-4o-mini"))
        
        start_time = time.time()
        
        try:
            response = self._call_llm(
                LLMProvider(provider), model, prompt, 
                system_prompt, temperature, max_tokens, json_mode
            )
        except Exception as e:
            if retry_on_failure:
                # Try fallback
                routing = self.TASK_ROUTING.get(task_type, {})
                fallback = routing.get("fallback")
                if fallback:
                    provider, model = fallback
                    response = self._call_llm(
                        LLMProvider(provider), model, prompt,
                        system_prompt, temperature, max_tokens, json_mode
                    )
                else:
                    raise
            else:
                raise
        
        latency = int((time.time() - start_time) * 1000)
        
        # Calculate cost
        pricing = self.PRICING.get(provider, {}).get(model, {"input": 0, "output": 0})
        cost = (
            (response["tokens_input"] / 1_000_000) * pricing["input"] +
            (response["tokens_output"] / 1_000_000) * pricing["output"]
        )
        
        return LLMResponse(
            content=response["content"],
            model=model,
            provider=provider,
            tokens_input=response["tokens_input"],
            tokens_output=response["tokens_output"],
            cost_usd=cost,
            latency_ms=latency,
            raw_response=response["raw"]
        )
    
    def _call_llm(self, provider: LLMProvider, model: str, prompt: str,
                  system_prompt: Optional[str], temperature: float,
                  max_tokens: int, json_mode: bool) -> Dict:
        """Call the appropriate LLM"""
        
        if provider == LLMProvider.OPENAI:
            return self._call_openai(model, prompt, system_prompt, 
                                     temperature, max_tokens, json_mode)
        elif provider == LLMProvider.GEMINI:
            return self._call_gemini(model, prompt, system_prompt,
                                     temperature, max_tokens, json_mode)
        elif provider == LLMProvider.CLAUDE:
            return self._call_claude(model, prompt, system_prompt,
                                     temperature, max_tokens, json_mode)
    
    def _call_openai(self, model: str, prompt: str, system_prompt: Optional[str],
                     temperature: float, max_tokens: int, json_mode: bool) -> Dict:
        """Call OpenAI API"""
        client = self.get_client(LLMProvider.OPENAI)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = client.chat.completions.create(**kwargs)
        
        return {
            "content": response.choices[0].message.content,
            "tokens_input": response.usage.prompt_tokens,
            "tokens_output": response.usage.completion_tokens,
            "raw": response.model_dump()
        }
    
    def _call_gemini(self, model: str, prompt: str, system_prompt: Optional[str],
                     temperature: float, max_tokens: int, json_mode: bool) -> Dict:
        """Call Gemini API"""
        client = self.get_client(LLMProvider.GEMINI)
        
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens
        }
        
        if json_mode:
            generation_config["response_mime_type"] = "application/json"
        
        model_instance = client.GenerativeModel(
            model_name=model,
            system_instruction=system_prompt,
            generation_config=generation_config
        )
        
        response = model_instance.generate_content(prompt)
        
        return {
            "content": response.text,
            "tokens_input": response.usage_metadata.prompt_token_count,
            "tokens_output": response.usage_metadata.candidates_token_count,
            "raw": {"text": response.text}
        }
    
    def _call_claude(self, model: str, prompt: str, system_prompt: Optional[str],
                     temperature: float, max_tokens: int, json_mode: bool) -> Dict:
        """Call Claude API"""
        client = self.get_client(LLMProvider.CLAUDE)
        
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        if temperature != 1.0:
            kwargs["temperature"] = temperature
        
        response = client.messages.create(**kwargs)
        
        return {
            "content": response.content[0].text,
            "tokens_input": response.usage.input_tokens,
            "tokens_output": response.usage.output_tokens,
            "raw": response.model_dump()
        }
```

### 5.2 Product Matching AI Agent

```python
# int/int/ai/agents/product_matcher.py

import json
from typing import Dict, List, Optional, Tuple
import frappe
from int.ai.router import INTAIRouter


class ProductMatcherAgent:
    """
    AI-powered product matching across marketplaces
    
    Uses multi-modal approach:
    1. Barcode/GTIN exact match
    2. SKU similarity
    3. Title semantic similarity
    4. Image similarity (optional)
    5. LLM-based attribute matching
    """
    
    SYSTEM_PROMPT = """You are an expert e-commerce product matcher. Your task is to determine if two products are the same item or variants of the same product.

Analyze the following attributes:
1. Product title/name
2. Brand
3. Category
4. Key attributes (color, size, material, etc.)
5. Description keywords

Return a JSON response with:
{
    "match_type": "exact" | "variant" | "similar" | "different",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation",
    "matched_attributes": ["attr1", "attr2"],
    "mismatched_attributes": ["attr3"],
    "suggested_mapping": {
        "source_field": "target_field"
    }
}

Be strict about brand matching - different brands = different products.
Consider variants (color/size) as matches with type "variant".
"""
    
    def __init__(self):
        self.router = INTAIRouter()
    
    def match_products(self, 
                       source_product: Dict,
                       target_products: List[Dict],
                       min_confidence: float = 0.7) -> List[Tuple[Dict, float, str]]:
        """
        Match a source product against multiple target products
        
        Returns: List of (product, confidence, match_type) tuples
        """
        # Stage 1: Quick filters (barcode, SKU)
        quick_matches = self._quick_match(source_product, target_products)
        if quick_matches:
            return quick_matches
        
        # Stage 2: Title-based pre-filtering
        candidates = self._title_prefilter(source_product, target_products)
        
        if not candidates:
            return []
        
        # Stage 3: AI-powered detailed matching
        matches = []
        for target in candidates[:10]:  # Limit to top 10 candidates
            result = self._ai_match(source_product, target)
            if result["confidence"] >= min_confidence:
                matches.append((target, result["confidence"], result["match_type"]))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def _quick_match(self, source: Dict, targets: List[Dict]) -> List[Tuple[Dict, float, str]]:
        """Quick exact matching by barcode/GTIN/SKU"""
        matches = []
        
        source_barcode = source.get("barcode", "").strip()
        source_gtin = source.get("gtin", "").strip()
        source_sku = source.get("sku", "").strip()
        
        for target in targets:
            target_barcode = target.get("barcode", "").strip()
            target_gtin = target.get("gtin", "").strip()
            
            # Barcode match
            if source_barcode and target_barcode and source_barcode == target_barcode:
                matches.append((target, 0.99, "exact"))
                continue
            
            # GTIN match
            if source_gtin and target_gtin and source_gtin == target_gtin:
                matches.append((target, 0.99, "exact"))
                continue
        
        return matches
    
    def _title_prefilter(self, source: Dict, targets: List[Dict], 
                         threshold: float = 0.3) -> List[Dict]:
        """Pre-filter by title similarity using simple text matching"""
        from difflib import SequenceMatcher
        
        source_title = source.get("title", "").lower()
        source_brand = source.get("brand", "").lower()
        
        scored = []
        for target in targets:
            target_title = target.get("title", "").lower()
            target_brand = target.get("brand", "").lower()
            
            # Brand must match (or be absent)
            if source_brand and target_brand and source_brand != target_brand:
                continue
            
            # Title similarity
            ratio = SequenceMatcher(None, source_title, target_title).ratio()
            if ratio >= threshold:
                scored.append((target, ratio))
        
        # Sort by similarity
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored]
    
    def _ai_match(self, source: Dict, target: Dict) -> Dict:
        """Use LLM for detailed product matching"""
        prompt = f"""Compare these two products and determine if they are the same item:

PRODUCT A (Source):
- Title: {source.get('title', 'N/A')}
- Brand: {source.get('brand', 'N/A')}
- Category: {source.get('category', 'N/A')}
- SKU: {source.get('sku', 'N/A')}
- Barcode: {source.get('barcode', 'N/A')}
- Attributes: {json.dumps(source.get('attributes', {}), ensure_ascii=False)}
- Description: {(source.get('description', '') or '')[:500]}

PRODUCT B (Target):
- Title: {target.get('title', 'N/A')}
- Brand: {target.get('brand', 'N/A')}
- Category: {target.get('category', 'N/A')}
- SKU: {target.get('sku', 'N/A')}
- Barcode: {target.get('barcode', 'N/A')}
- Attributes: {json.dumps(target.get('attributes', {}), ensure_ascii=False)}
- Description: {(target.get('description', '') or '')[:500]}

Are these the same product or variants of the same product?"""

        response = self.router.complete(
            prompt=prompt,
            task_type="product_matching",
            system_prompt=self.SYSTEM_PROMPT,
            json_mode=True,
            temperature=0.3  # Lower temperature for consistency
        )
        
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            result = {
                "match_type": "different",
                "confidence": 0.0,
                "reasoning": "Failed to parse AI response"
            }
        
        # Log the AI task
        frappe.get_doc({
            "doctype": "INT AI Task",
            "task_type": "Product_Matching",
            "input_data": {"source": source, "target": target},
            "output_data": result,
            "model_used": response.model,
            "tokens_input": response.tokens_input,
            "tokens_output": response.tokens_output,
            "cost_usd": response.cost_usd,
            "confidence_score": result.get("confidence", 0) * 100,
            "status": "Completed"
        }).insert(ignore_permissions=True)
        
        return result
    
    def bulk_match(self, source_products: List[Dict], 
                   target_marketplace: str,
                   batch_size: int = 50) -> Dict[str, Dict]:
        """
        Bulk match products against a marketplace
        
        Returns: {source_id: {"target": product, "confidence": float, "type": str}}
        """
        # Get target products from marketplace
        connector_name = frappe.db.get_value(
            "INT Connector", 
            {"platform": target_marketplace, "enabled": 1}
        )
        
        if not connector_name:
            frappe.throw(f"No active connector for {target_marketplace}")
        
        from int.connectors import get_connector
        connector = get_connector(connector_name)
        
        # Fetch all target products (paginated)
        all_targets = []
        page = 0
        while True:
            targets = connector.get_products(page=page, page_size=100)
            if not targets:
                break
            all_targets.extend(targets)
            page += 1
            
            if len(all_targets) >= 10000:  # Safety limit
                break
        
        # Match each source product
        results = {}
        for source in source_products:
            matches = self.match_products(source, all_targets)
            if matches:
                best = matches[0]
                results[source.get("id") or source.get("sku")] = {
                    "target": best[0],
                    "confidence": best[1],
                    "type": best[2]
                }
        
        return results
```

### 5.3 Natural Language Configuration

```python
# int/int/ai/agents/nl_config.py

import json
from typing import Dict, Optional
import frappe
from int.ai.router import INTAIRouter


class NLConfigAgent:
    """
    Natural Language to Configuration converter
    
    Examples:
    - "Trendyol siparişlerini 60 dakika beklet sonra kargoya ver"
    - "Stok 5'in altına düşünce beni bilgilendir"
    - "Her gün saat 9'da fiyatları güncelle"
    """
    
    SYSTEM_PROMPT = """You are an e-commerce automation configuration assistant. Convert natural language requests into structured workflow configurations.

Available actions:
- sync_products: Sync products to/from marketplace
- sync_orders: Sync orders
- sync_inventory: Update inventory levels
- sync_prices: Update prices
- send_notification: Send email/SMS/webhook notification
- delay: Wait for specified time
- condition: Check a condition
- transform_data: Transform data format
- create_document: Create Frappe document
- update_document: Update Frappe document
- call_api: Make HTTP request
- ai_process: Use AI for processing

Available triggers:
- event: On document event (order.created, product.updated, etc.)
- schedule: Cron schedule
- webhook: On webhook received
- manual: Manual trigger

Return a JSON workflow configuration:
{
    "workflow_name": "descriptive name",
    "description": "what this workflow does",
    "trigger_type": "event|schedule|webhook|manual",
    "trigger_config": {
        // trigger-specific config
    },
    "nodes": [
        {
            "node_id": "unique_id",
            "node_type": "action type",
            "node_name": "descriptive name",
            "config": {
                // node-specific config
            },
            "next": ["next_node_id"] // or null for end
        }
    ]
}

For Turkish language input, translate to English internally but keep user-facing strings in Turkish.
"""

    def __init__(self):
        self.router = INTAIRouter()
    
    def parse_request(self, natural_language: str, 
                      context: Optional[Dict] = None) -> Dict:
        """
        Convert natural language to workflow configuration
        """
        context_str = ""
        if context:
            context_str = f"""

Context:
- Available connectors: {', '.join(context.get('connectors', []))}
- Available workflows: {', '.join(context.get('workflows', []))}
- User role: {context.get('user_role', 'User')}
"""
        
        prompt = f"""Convert this request to a workflow configuration:

"{natural_language}"
{context_str}

Generate a complete, valid workflow JSON."""

        response = self.router.complete(
            prompt=prompt,
            task_type="natural_language_query",
            system_prompt=self.SYSTEM_PROMPT,
            json_mode=True,
            temperature=0.5
        )
        
        try:
            config = json.loads(response.content)
            
            # Validate and enhance
            config = self._validate_config(config)
            config = self._add_default_error_handling(config)
            
            return {
                "success": True,
                "config": config,
                "interpretation": self._generate_interpretation(config),
                "tokens_used": response.tokens_input + response.tokens_output,
                "cost": response.cost_usd
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse configuration: {str(e)}",
                "raw_response": response.content
            }
    
    def _validate_config(self, config: Dict) -> Dict:
        """Validate and fix configuration"""
        # Ensure required fields
        if "workflow_name" not in config:
            config["workflow_name"] = "Auto-generated Workflow"
        
        if "trigger_type" not in config:
            config["trigger_type"] = "manual"
        
        if "nodes" not in config:
            config["nodes"] = []
        
        # Generate node IDs if missing
        for i, node in enumerate(config["nodes"]):
            if "node_id" not in node:
                node["node_id"] = f"node_{i+1}"
        
        return config
    
    def _add_default_error_handling(self, config: Dict) -> Dict:
        """Add default error handling if not present"""
        if "error_handling" not in config:
            config["error_handling"] = "Notify"
        
        return config
    
    def _generate_interpretation(self, config: Dict) -> str:
        """Generate human-readable interpretation"""
        parts = [f"**Workflow**: {config.get('workflow_name', 'Unnamed')}"]
        
        trigger = config.get("trigger_type", "manual")
        trigger_config = config.get("trigger_config", {})
        
        if trigger == "event":
            parts.append(f"**Trigger**: When {trigger_config.get('event_type', 'event')} occurs")
        elif trigger == "schedule":
            parts.append(f"**Trigger**: Scheduled ({trigger_config.get('cron', 'not set')})")
        else:
            parts.append(f"**Trigger**: {trigger.title()}")
        
        parts.append(f"**Steps**: {len(config.get('nodes', []))} actions")
        
        for node in config.get("nodes", []):
            parts.append(f"  - {node.get('node_name', node.get('node_type', 'Unknown'))}")
        
        return "\n".join(parts)
    
    def create_workflow(self, natural_language: str,
                        auto_enable: bool = False) -> Dict:
        """
        Create workflow from natural language and save to database
        """
        result = self.parse_request(natural_language)
        
        if not result["success"]:
            return result
        
        config = result["config"]
        
        # Create workflow document
        workflow = frappe.get_doc({
            "doctype": "INT Workflow",
            "workflow_name": config["workflow_name"],
            "description": config.get("description", natural_language),
            "enabled": auto_enable,
            "trigger_type": config["trigger_type"],
            "trigger_config": config.get("trigger_config", {}),
            "error_handling": config.get("error_handling", "Notify")
        })
        
        # Add nodes
        for node_config in config.get("nodes", []):
            workflow.append("nodes", {
                "node_id": node_config["node_id"],
                "node_type": node_config["node_type"],
                "node_name": node_config.get("node_name", node_config["node_type"]),
                "config": node_config.get("config", {}),
                "position_x": node_config.get("position_x", 0),
                "position_y": node_config.get("position_y", 0)
            })
        
        # Add connections
        for node_config in config.get("nodes", []):
            next_nodes = node_config.get("next", [])
            if next_nodes:
                for next_id in (next_nodes if isinstance(next_nodes, list) else [next_nodes]):
                    workflow.append("connections", {
                        "from_node": node_config["node_id"],
                        "to_node": next_id
                    })
        
        workflow.insert()
        
        return {
            "success": True,
            "workflow": workflow.name,
            "interpretation": result["interpretation"],
            "config": config
        }


# Example usage:
# agent = NLConfigAgent()
# result = agent.create_workflow(
#     "Trendyol'dan yeni sipariş geldiğinde, stoku kontrol et, "
#     "stok varsa ERPNext'te satış siparişi oluştur ve bana email at",
#     auto_enable=False
# )
```

---

## 6. Event-Driven Architecture (EDA)

### 6.1 Event Bus Implementation

```python
# int/int/events/bus.py

import json
from typing import Dict, Callable, Optional, List
from dataclasses import dataclass
from datetime import datetime
import frappe
import redis


@dataclass
class Event:
    event_id: str
    event_type: str
    source: str
    connector: Optional[str]
    payload: Dict
    correlation_id: Optional[str]
    causation_id: Optional[str]
    timestamp: datetime


class EventBus:
    """
    Redis Streams based event bus for INT
    """
    
    STREAM_PREFIX = "int:events:"
    CONSUMER_GROUP = "int_workers"
    
    def __init__(self):
        self.redis = self._get_redis_client()
        self._handlers: Dict[str, List[Callable]] = {}
        self._ensure_streams()
    
    def _get_redis_client(self) -> redis.Redis:
        """Get Redis client from Frappe config"""
        redis_url = frappe.conf.get("redis_queue") or "redis://localhost:6379"
        return redis.from_url(redis_url, decode_responses=True)
    
    def _ensure_streams(self):
        """Ensure consumer groups exist for all event streams"""
        event_types = [
            "order", "product", "inventory", "price",
            "shipment", "return", "sync", "error"
        ]
        
        for event_type in event_types:
            stream = f"{self.STREAM_PREFIX}{event_type}"
            try:
                self.redis.xgroup_create(
                    stream, 
                    self.CONSUMER_GROUP, 
                    id="0", 
                    mkstream=True
                )
            except redis.ResponseError as e:
                if "BUSYGROUP" not in str(e):
                    raise
    
    def publish(self, event: Event) -> str:
        """
        Publish an event to the appropriate stream
        """
        # Determine stream from event type
        stream_type = event.event_type.split(".")[0]
        stream = f"{self.STREAM_PREFIX}{stream_type}"
        
        # Serialize event
        event_data = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            "connector": event.connector or "",
            "payload": json.dumps(event.payload),
            "correlation_id": event.correlation_id or "",
            "causation_id": event.causation_id or "",
            "timestamp": event.timestamp.isoformat()
        }
        
        # Add to stream
        message_id = self.redis.xadd(stream, event_data)
        
        # Also persist to database for audit
        self._persist_event(event)
        
        return message_id
    
    def _persist_event(self, event: Event):
        """Persist event to database"""
        frappe.get_doc({
            "doctype": "INT Event",
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            "connector": event.connector,
            "payload": event.payload,
            "correlation_id": event.correlation_id,
            "causation_id": event.causation_id
        }).insert(ignore_permissions=True)
    
    def subscribe(self, event_pattern: str, handler: Callable):
        """
        Subscribe to events matching pattern
        
        Patterns:
        - "order.*" - all order events
        - "product.created" - specific event
        - "*" - all events
        """
        if event_pattern not in self._handlers:
            self._handlers[event_pattern] = []
        self._handlers[event_pattern].append(handler)
    
    def consume(self, consumer_name: str, count: int = 10, 
                block: int = 5000) -> List[Event]:
        """
        Consume events from all streams
        """
        events = []
        
        # Get all streams
        streams = {
            f"{self.STREAM_PREFIX}{t}": ">" 
            for t in ["order", "product", "inventory", "price", 
                      "shipment", "return", "sync", "error"]
        }
        
        # Read from streams
        try:
            results = self.redis.xreadgroup(
                self.CONSUMER_GROUP,
                consumer_name,
                streams,
                count=count,
                block=block
            )
        except redis.ResponseError:
            return events
        
        if not results:
            return events
        
        for stream_name, messages in results:
            for message_id, data in messages:
                event = Event(
                    event_id=data["event_id"],
                    event_type=data["event_type"],
                    source=data["source"],
                    connector=data["connector"] or None,
                    payload=json.loads(data["payload"]),
                    correlation_id=data["correlation_id"] or None,
                    causation_id=data["causation_id"] or None,
                    timestamp=datetime.fromisoformat(data["timestamp"])
                )
                event._message_id = message_id
                event._stream = stream_name
                events.append(event)
        
        return events
    
    def ack(self, event: Event):
        """Acknowledge event processing"""
        if hasattr(event, "_stream") and hasattr(event, "_message_id"):
            self.redis.xack(event._stream, self.CONSUMER_GROUP, event._message_id)
    
    def dispatch(self, event: Event):
        """Dispatch event to registered handlers"""
        for pattern, handlers in self._handlers.items():
            if self._matches_pattern(event.event_type, pattern):
                for handler in handlers:
                    try:
                        handler(event)
                    except Exception as e:
                        frappe.log_error(
                            f"Event handler error: {str(e)}",
                            f"INT Event: {event.event_type}"
                        )
    
    def _matches_pattern(self, event_type: str, pattern: str) -> bool:
        """Check if event type matches pattern"""
        if pattern == "*":
            return True
        
        if pattern.endswith(".*"):
            prefix = pattern[:-2]
            return event_type.startswith(prefix + ".")
        
        return event_type == pattern


# Global event bus instance
_event_bus = None

def get_event_bus() -> EventBus:
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


def emit_event(event_type: str, payload: Dict, 
               connector: Optional[str] = None,
               source: str = "System",
               correlation_id: Optional[str] = None,
               causation_id: Optional[str] = None) -> str:
    """
    Convenience function to emit an event
    """
    event = Event(
        event_id=frappe.generate_hash(length=32),
        event_type=event_type,
        source=source,
        connector=connector,
        payload=payload,
        correlation_id=correlation_id,
        causation_id=causation_id,
        timestamp=datetime.now()
    )
    
    bus = get_event_bus()
    return bus.publish(event)
```

### 6.2 Event Worker

```python
# int/int/events/worker.py

import frappe
from frappe.utils.background_jobs import get_jobs
from int.events.bus import get_event_bus, Event
from int.events.handlers import get_handler


def start_event_worker():
    """
    Start the event worker process
    Call this from bench console or as background job
    """
    worker = EventWorker()
    worker.run()


class EventWorker:
    """
    Event worker that processes events from the bus
    """
    
    def __init__(self):
        self.bus = get_event_bus()
        self.consumer_name = f"worker_{frappe.generate_hash(length=8)}"
        self.running = True
    
    def run(self):
        """Main worker loop"""
        frappe.logger().info(f"INT Event Worker started: {self.consumer_name}")
        
        while self.running:
            try:
                events = self.bus.consume(self.consumer_name, count=10, block=5000)
                
                for event in events:
                    self.process_event(event)
                    
            except Exception as e:
                frappe.log_error(f"Event worker error: {str(e)}", "INT Event Worker")
                import time
                time.sleep(5)  # Backoff on error
    
    def process_event(self, event: Event):
        """Process a single event"""
        try:
            # Get handler for event type
            handler = get_handler(event.event_type)
            
            if handler:
                # Process the event
                result = handler(event)
                
                # Update event record
                self._update_event_status(event, "Completed", result)
            else:
                frappe.logger().warning(f"No handler for event: {event.event_type}")
            
            # Acknowledge the event
            self.bus.ack(event)
            
        except Exception as e:
            frappe.log_error(f"Event processing error: {str(e)}", 
                           f"INT Event: {event.event_id}")
            self._update_event_status(event, "Failed", {"error": str(e)})
            
            # Handle retry logic
            self._handle_retry(event, str(e))
    
    def _update_event_status(self, event: Event, status: str, result: Dict = None):
        """Update event record in database"""
        event_doc = frappe.get_doc("INT Event", {"event_id": event.event_id})
        event_doc.processed = (status == "Completed")
        event_doc.processed_at = frappe.utils.now_datetime()
        event_doc.processing_attempts += 1
        
        if status == "Failed":
            event_doc.last_error = str(result.get("error", "Unknown error"))
        
        event_doc.save(ignore_permissions=True)
    
    def _handle_retry(self, event: Event, error: str):
        """Handle event retry logic"""
        settings = frappe.get_single("INT Settings")
        max_retries = settings.max_retry_attempts or 3
        
        event_doc = frappe.get_doc("INT Event", {"event_id": event.event_id})
        
        if event_doc.processing_attempts >= max_retries:
            # Move to dead letter queue
            event_doc.dead_letter = True
            event_doc.save(ignore_permissions=True)
            
            # Emit dead letter event
            from int.events.bus import emit_event
            emit_event(
                "error.dead_letter",
                {
                    "original_event_id": event.event_id,
                    "original_event_type": event.event_type,
                    "error": error,
                    "attempts": event_doc.processing_attempts
                },
                connector=event.connector
            )
        else:
            # Re-queue for retry with backoff
            delay = settings.retry_backoff_multiplier ** event_doc.processing_attempts
            frappe.enqueue(
                "int.events.worker.retry_event",
                event_id=event.event_id,
                queue="long",
                timeout=300,
                at_front=False,
                enqueue_after_commit=True,
                job_name=f"INT Retry: {event.event_id}",
                at=frappe.utils.add_to_date(None, seconds=int(delay))
            )
    
    def stop(self):
        """Stop the worker gracefully"""
        self.running = False


def retry_event(event_id: str):
    """Retry a failed event"""
    event_doc = frappe.get_doc("INT Event", {"event_id": event_id})
    
    event = Event(
        event_id=event_doc.event_id,
        event_type=event_doc.event_type,
        source=event_doc.source,
        connector=event_doc.connector,
        payload=event_doc.payload,
        correlation_id=event_doc.correlation_id,
        causation_id=event_doc.causation_id,
        timestamp=frappe.utils.now_datetime()
    )
    
    worker = EventWorker()
    worker.process_event(event)
```

---

## 7. API Design

### 7.1 REST API Endpoints

```python
# int/int/api/v1/__init__.py

import frappe
from frappe import _
from frappe.utils import cint, cstr
from typing import Dict, List, Optional


# ==================== CONNECTOR APIs ====================

@frappe.whitelist()
def get_connectors(enabled_only: bool = True) -> List[Dict]:
    """
    Get list of configured connectors
    
    GET /api/method/int.api.v1.get_connectors
    """
    filters = {}
    if enabled_only:
        filters["enabled"] = 1
    
    connectors = frappe.get_all(
        "INT Connector",
        filters=filters,
        fields=["name", "connector_name", "connector_type", "platform",
                "enabled", "sync_status", "last_sync_at"]
    )
    
    return connectors


@frappe.whitelist()
def test_connector(connector: str) -> Dict:
    """
    Test connector connection
    
    POST /api/method/int.api.v1.test_connector
    """
    from int.connectors import get_connector
    
    try:
        conn = get_connector(connector)
        # Try a simple API call
        conn.get_categories()
        return {"success": True, "message": _("Connection successful")}
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def sync_connector(connector: str, sync_type: str = "all") -> Dict:
    """
    Trigger sync for a connector
    
    POST /api/method/int.api.v1.sync_connector
    
    sync_type: all, products, orders, inventory, prices
    """
    frappe.enqueue(
        "int.tasks.sync.run_sync",
        connector=connector,
        sync_type=sync_type,
        queue="long",
        timeout=3600,
        job_name=f"INT Sync: {connector}"
    )
    
    return {"success": True, "message": _("Sync started")}


# ==================== PRODUCT APIs ====================

@frappe.whitelist()
def get_product_mappings(connector: Optional[str] = None,
                         status: Optional[str] = None,
                         page: int = 1,
                         page_size: int = 50) -> Dict:
    """
    Get product mappings with pagination
    
    GET /api/method/int.api.v1.get_product_mappings
    """
    filters = {}
    if connector:
        filters["connector"] = connector
    if status:
        filters["listing_status"] = status
    
    count = frappe.db.count("INT Product Mapping", filters)
    
    mappings = frappe.get_all(
        "INT Product Mapping",
        filters=filters,
        fields=["name", "pim_product", "connector", "marketplace_product_id",
                "marketplace_sku", "listing_status", "match_confidence",
                "match_method", "last_synced_at"],
        start=(page - 1) * page_size,
        page_length=page_size,
        order_by="modified desc"
    )
    
    return {
        "data": mappings,
        "total": count,
        "page": page,
        "page_size": page_size,
        "total_pages": (count + page_size - 1) // page_size
    }


@frappe.whitelist()
def match_products(pim_products: List[str], 
                   connector: str,
                   auto_map: bool = False) -> Dict:
    """
    AI-powered product matching
    
    POST /api/method/int.api.v1.match_products
    """
    from int.ai.agents.product_matcher import ProductMatcherAgent
    
    agent = ProductMatcherAgent()
    
    results = {}
    for pim_product in pim_products:
        # Get PIM product data
        product_data = frappe.get_doc("PIM Product", pim_product).as_dict()
        
        # Get connector
        from int.connectors import get_connector
        conn = get_connector(connector)
        
        # Get marketplace products
        marketplace_products = conn.get_products()
        
        # Match
        matches = agent.match_products(product_data, marketplace_products)
        
        results[pim_product] = {
            "matches": [
                {
                    "marketplace_id": m[0].get("id") or m[0].get("barcode"),
                    "title": m[0].get("title"),
                    "confidence": m[1],
                    "match_type": m[2]
                }
                for m in matches[:5]  # Top 5 matches
            ]
        }
        
        # Auto-map if requested and high confidence match found
        if auto_map and matches and matches[0][1] >= 0.9:
            best_match = matches[0]
            _create_mapping(pim_product, connector, best_match[0], best_match[1], best_match[2])
            results[pim_product]["auto_mapped"] = True
    
    return results


def _create_mapping(pim_product: str, connector: str, 
                    marketplace_product: Dict, confidence: float, match_type: str):
    """Create product mapping"""
    if frappe.db.exists("INT Product Mapping", 
                       {"pim_product": pim_product, "connector": connector}):
        return
    
    frappe.get_doc({
        "doctype": "INT Product Mapping",
        "pim_product": pim_product,
        "connector": connector,
        "marketplace_product_id": marketplace_product.get("id") or marketplace_product.get("barcode"),
        "marketplace_sku": marketplace_product.get("sku") or marketplace_product.get("stockCode"),
        "marketplace_barcode": marketplace_product.get("barcode"),
        "listing_status": "Active",
        "match_confidence": confidence * 100,
        "match_method": f"AI_Matched ({match_type})",
        "sync_enabled": True
    }).insert(ignore_permissions=True)


# ==================== ORDER APIs ====================

@frappe.whitelist()
def get_orders(connector: Optional[str] = None,
               status: Optional[str] = None,
               start_date: Optional[str] = None,
               end_date: Optional[str] = None,
               page: int = 1,
               page_size: int = 50) -> Dict:
    """
    Get marketplace orders
    
    GET /api/method/int.api.v1.get_orders
    """
    filters = {}
    if connector:
        filters["connector"] = connector
    if status:
        filters["int_status"] = status
    if start_date:
        filters["order_date"] = [">=", start_date]
    if end_date:
        filters["order_date"] = ["<=", end_date]
    
    count = frappe.db.count("INT Order", filters)
    
    orders = frappe.get_all(
        "INT Order",
        filters=filters,
        fields=["name", "order_id", "connector", "sales_order",
                "marketplace_status", "int_status", "order_date",
                "customer_name", "total_amount", "currency"],
        start=(page - 1) * page_size,
        page_length=page_size,
        order_by="order_date desc"
    )
    
    return {
        "data": orders,
        "total": count,
        "page": page,
        "page_size": page_size
    }


@frappe.whitelist()
def ship_order(order: str, tracking_number: str,
               cargo_company: Optional[str] = None) -> Dict:
    """
    Mark order as shipped
    
    POST /api/method/int.api.v1.ship_order
    """
    order_doc = frappe.get_doc("INT Order", order)
    
    from int.connectors import get_connector
    conn = get_connector(order_doc.connector)
    
    result = conn.create_shipment(
        order_doc.order_id,
        {
            "tracking_number": tracking_number,
            "cargo_company": cargo_company
        }
    )
    
    order_doc.int_status = "Shipped"
    order_doc.tracking_numbers = tracking_number
    order_doc.save()
    
    return {"success": True, "result": result}


# ==================== WORKFLOW APIs ====================

@frappe.whitelist()
def execute_workflow(workflow: str, inputs: Optional[Dict] = None) -> Dict:
    """
    Manually execute a workflow
    
    POST /api/method/int.api.v1.execute_workflow
    """
    from int.workflows.engine import WorkflowEngine
    
    engine = WorkflowEngine(workflow)
    result = engine.execute(inputs or {})
    
    return result


@frappe.whitelist()
def create_workflow_from_nl(description: str, 
                            auto_enable: bool = False) -> Dict:
    """
    Create workflow from natural language
    
    POST /api/method/int.api.v1.create_workflow_from_nl
    """
    from int.ai.agents.nl_config import NLConfigAgent
    
    agent = NLConfigAgent()
    result = agent.create_workflow(description, auto_enable)
    
    return result


# ==================== AI APIs ====================

@frappe.whitelist()
def ai_query(query: str, context: Optional[Dict] = None) -> Dict:
    """
    Natural language query about data
    
    POST /api/method/int.api.v1.ai_query
    
    Examples:
    - "Bugün kaç sipariş geldi?"
    - "En çok satan 10 ürünü göster"
    - "Trendyol'daki stok uyumsuzluklarını listele"
    """
    from int.ai.agents.query_agent import QueryAgent
    
    agent = QueryAgent()
    result = agent.execute(query, context)
    
    return result


# ==================== WEBHOOK HANDLER ====================

@frappe.whitelist(allow_guest=True)
def webhook_handler(connector: str):
    """
    Handle incoming webhooks from marketplaces
    
    POST /api/method/int.api.v1.webhook_handler/{connector}
    """
    import json
    
    # Get request data
    if frappe.request.data:
        payload = json.loads(frappe.request.data)
    else:
        payload = frappe.form_dict
    
    headers = dict(frappe.request.headers)
    
    # Get connector and handle webhook
    from int.connectors import get_connector
    conn = get_connector(connector)
    
    result = conn.handle_webhook(payload, headers)
    
    return result
```

### 7.2 GraphQL API (Optional)

```python
# int/int/api/graphql/__init__.py

"""
GraphQL API for INT
Requires frappe-graphql app
"""

import frappe
from frappe_graphql import make_schema


# Schema definitions in SDL
SDL = """
type Query {
    connectors(enabled: Boolean): [Connector!]!
    connector(name: String!): Connector
    productMappings(connector: String, status: String, page: Int, pageSize: Int): ProductMappingConnection!
    orders(connector: String, status: String, startDate: String, endDate: String, page: Int, pageSize: Int): OrderConnection!
    workflows(enabled: Boolean): [Workflow!]!
    aiTask(id: String!): AITask
}

type Mutation {
    syncConnector(connector: String!, syncType: SyncType!): SyncResult!
    matchProducts(pimProducts: [String!]!, connector: String!, autoMap: Boolean): ProductMatchResult!
    shipOrder(order: String!, trackingNumber: String!, cargoCompany: String): ShipResult!
    createWorkflowFromNL(description: String!, autoEnable: Boolean): WorkflowCreateResult!
    executeWorkflow(workflow: String!, inputs: JSON): WorkflowExecuteResult!
}

type Subscription {
    syncProgress(connector: String!): SyncProgress!
    orderCreated(connector: String): Order!
    eventStream(eventTypes: [String!]): Event!
}

type Connector {
    name: String!
    connectorName: String!
    connectorType: ConnectorType!
    platform: String!
    enabled: Boolean!
    syncStatus: SyncStatus!
    lastSyncAt: DateTime
    productMappings: [ProductMapping!]!
    orders: [Order!]!
}

type ProductMapping {
    name: String!
    pimProduct: String!
    connector: Connector!
    marketplaceProductId: String
    marketplaceSku: String
    listingStatus: ListingStatus!
    matchConfidence: Float
    matchMethod: String
    lastSyncedAt: DateTime
}

type Order {
    name: String!
    orderId: String!
    connector: Connector!
    salesOrder: String
    marketplaceStatus: String
    intStatus: OrderStatus!
    orderDate: DateTime!
    customerName: String
    totalAmount: Float!
    currency: String!
    items: [OrderItem!]!
}

# ... more type definitions
"""

def get_schema():
    return make_schema(SDL, resolvers)


resolvers = {
    "Query": {
        "connectors": lambda _, info, enabled=True: frappe.get_all(
            "INT Connector",
            filters={"enabled": 1} if enabled else {},
            fields=["*"]
        ),
        # ... more resolvers
    },
    "Mutation": {
        "syncConnector": lambda _, info, connector, syncType: {
            "success": True
        },
        # ... more resolvers
    }
}
```

---

## 8. Frappe AI Ecosystem Integration

### 8.1 KAI (CrewAI) Integration

```python
# int/int/ai/kai_integration.py

"""
Integration with KAI (KorucuTech/kai) for CrewAI support
https://github.com/KorucuTech/kai
"""

import frappe


def create_kai_crew_from_int(int_crew_name: str) -> str:
    """
    Create a KAI Crew from INT AI Crew definition
    """
    int_crew = frappe.get_doc("INT AI Crew", int_crew_name)
    
    # Create KAI Crew
    kai_crew = frappe.get_doc({
        "doctype": "KAI Crew",
        "crew_name": int_crew.crew_name,
        "process": int_crew.process.lower(),  # sequential/hierarchical
        "verbose": int_crew.verbose,
        "memory": int_crew.memory
    })
    
    # Add agents
    for int_agent in int_crew.agents:
        agent_doc = frappe.get_doc("INT AI Agent", int_agent.agent)
        
        kai_crew.append("agents", {
            "agent": create_kai_agent(agent_doc)
        })
    
    # Add tasks
    for int_task in int_crew.tasks:
        kai_crew.append("tasks", {
            "task_name": int_task.task_name,
            "description": int_task.description,
            "expected_output": int_task.expected_output,
            "agent": int_task.agent
        })
    
    kai_crew.insert()
    return kai_crew.name


def create_kai_agent(int_agent) -> str:
    """
    Create a KAI Agent from INT AI Agent
    """
    # Map LLM provider to KAI LLM
    llm_mapping = {
        "OpenAI": f"openai/{int_agent.llm_model}",
        "Gemini": f"google/{int_agent.llm_model}",
        "Claude": f"anthropic/{int_agent.llm_model}"
    }
    
    kai_agent = frappe.get_doc({
        "doctype": "KAI Agent",
        "agent_name": int_agent.agent_name,
        "role": int_agent.role,
        "goal": int_agent.goal,
        "backstory": int_agent.backstory,
        "llm": llm_mapping.get(int_agent.llm_provider, "openai/gpt-4o-mini"),
        "verbose": int_agent.verbose,
        "allow_delegation": int_agent.allow_delegation,
        "max_iter": int_agent.max_iterations
    })
    
    # Add tools
    for int_tool in int_agent.tools:
        kai_agent.append("tools", {
            "tool": create_kai_tool(int_tool)
        })
    
    kai_agent.insert()
    return kai_agent.name


def create_kai_tool(int_tool) -> str:
    """
    Create a KAI Tool from INT AI Tool
    """
    # Check if tool already exists
    existing = frappe.db.exists("KAI Tool", {"tool_name": int_tool.tool_name})
    if existing:
        return existing
    
    kai_tool = frappe.get_doc({
        "doctype": "KAI Tool",
        "tool_name": int_tool.tool_name,
        "description": int_tool.description,
        "function_code": int_tool.function_code
    })
    kai_tool.insert()
    return kai_tool.name


def run_kai_crew(kai_crew_name: str, inputs: dict) -> dict:
    """
    Execute a KAI Crew
    """
    crew = frappe.get_doc("KAI Crew", kai_crew_name)
    output = crew.kickoff(inputs=inputs)
    return {"result": str(output)}
```

### 8.2 MCP Server Integration

```python
# int/int/ai/mcp_integration.py

"""
MCP (Model Context Protocol) server for INT
Allows AI assistants to interact with INT data
"""

import frappe
from typing import Dict, List, Any


class INTMCPServer:
    """
    MCP Server exposing INT functionality to AI models
    
    Tools exposed:
    - get_connectors: List configured connectors
    - get_orders: Fetch orders with filters
    - get_products: Fetch product mappings
    - sync_connector: Trigger sync
    - ship_order: Mark order as shipped
    - create_workflow: Create automation workflow
    """
    
    def __init__(self):
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, Dict]:
        """Register available MCP tools"""
        return {
            "get_connectors": {
                "description": "Get list of configured marketplace connectors",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "enabled_only": {
                            "type": "boolean",
                            "description": "Only return enabled connectors",
                            "default": True
                        }
                    }
                },
                "handler": self._get_connectors
            },
            "get_orders": {
                "description": "Fetch marketplace orders with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "connector": {"type": "string", "description": "Connector name"},
                        "status": {"type": "string", "description": "Order status filter"},
                        "limit": {"type": "integer", "description": "Max orders to return", "default": 50}
                    }
                },
                "handler": self._get_orders
            },
            "get_product_mappings": {
                "description": "Get product mappings between PIM and marketplaces",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "connector": {"type": "string"},
                        "status": {"type": "string"},
                        "limit": {"type": "integer", "default": 50}
                    }
                },
                "handler": self._get_product_mappings
            },
            "sync_connector": {
                "description": "Trigger synchronization for a connector",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "connector": {"type": "string", "description": "Connector name"},
                        "sync_type": {
                            "type": "string",
                            "enum": ["all", "products", "orders", "inventory", "prices"],
                            "default": "all"
                        }
                    },
                    "required": ["connector"]
                },
                "handler": self._sync_connector
            },
            "ship_order": {
                "description": "Mark an order as shipped with tracking info",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order": {"type": "string", "description": "Order name/ID"},
                        "tracking_number": {"type": "string"},
                        "cargo_company": {"type": "string"}
                    },
                    "required": ["order", "tracking_number"]
                },
                "handler": self._ship_order
            },
            "get_sync_stats": {
                "description": "Get synchronization statistics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "connector": {"type": "string"},
                        "days": {"type": "integer", "default": 7}
                    }
                },
                "handler": self._get_sync_stats
            },
            "natural_language_query": {
                "description": "Execute natural language query about INT data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Natural language question"}
                    },
                    "required": ["query"]
                },
                "handler": self._nl_query
            }
        }
    
    def get_tool_definitions(self) -> List[Dict]:
        """Return tool definitions in MCP format"""
        return [
            {
                "name": name,
                "description": tool["description"],
                "inputSchema": tool["parameters"]
            }
            for name, tool in self.tools.items()
        ]
    
    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Execute a tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        handler = self.tools[tool_name]["handler"]
        return handler(**arguments)
    
    # Tool handlers
    def _get_connectors(self, enabled_only: bool = True) -> List[Dict]:
        filters = {"enabled": 1} if enabled_only else {}
        return frappe.get_all(
            "INT Connector",
            filters=filters,
            fields=["name", "connector_name", "connector_type", 
                    "platform", "enabled", "sync_status", "last_sync_at"]
        )
    
    def _get_orders(self, connector: str = None, status: str = None, 
                    limit: int = 50) -> List[Dict]:
        filters = {}
        if connector:
            filters["connector"] = connector
        if status:
            filters["int_status"] = status
        
        return frappe.get_all(
            "INT Order",
            filters=filters,
            fields=["name", "order_id", "connector", "int_status",
                    "order_date", "customer_name", "total_amount"],
            limit=limit,
            order_by="order_date desc"
        )
    
    def _get_product_mappings(self, connector: str = None, 
                              status: str = None, limit: int = 50) -> List[Dict]:
        filters = {}
        if connector:
            filters["connector"] = connector
        if status:
            filters["listing_status"] = status
        
        return frappe.get_all(
            "INT Product Mapping",
            filters=filters,
            fields=["name", "pim_product", "connector", "marketplace_sku",
                    "listing_status", "match_confidence"],
            limit=limit
        )
    
    def _sync_connector(self, connector: str, sync_type: str = "all") -> Dict:
        frappe.enqueue(
            "int.tasks.sync.run_sync",
            connector=connector,
            sync_type=sync_type,
            queue="long"
        )
        return {"success": True, "message": f"Sync started for {connector}"}
    
    def _ship_order(self, order: str, tracking_number: str, 
                    cargo_company: str = None) -> Dict:
        from int.api.v1 import ship_order
        return ship_order(order, tracking_number, cargo_company)
    
    def _get_sync_stats(self, connector: str = None, days: int = 7) -> Dict:
        from frappe.utils import add_days, today
        
        filters = {"started_at": [">=", add_days(today(), -days)]}
        if connector:
            filters["connector"] = connector
        
        logs = frappe.get_all(
            "INT Sync Log",
            filters=filters,
            fields=["connector", "operation", "status", 
                    "records_processed", "records_failed"]
        )
        
        # Aggregate stats
        stats = {
            "total_syncs": len(logs),
            "successful": len([l for l in logs if l["status"] == "Completed"]),
            "failed": len([l for l in logs if l["status"] == "Failed"]),
            "records_processed": sum(l.get("records_processed", 0) for l in logs),
            "records_failed": sum(l.get("records_failed", 0) for l in logs)
        }
        
        return stats
    
    def _nl_query(self, query: str) -> Dict:
        from int.ai.agents.query_agent import QueryAgent
        agent = QueryAgent()
        return agent.execute(query)


# Expose MCP server endpoint
@frappe.whitelist(allow_guest=True)
def mcp_endpoint():
    """MCP protocol endpoint"""
    import json
    
    data = json.loads(frappe.request.data)
    method = data.get("method")
    
    server = INTMCPServer()
    
    if method == "tools/list":
        return {"tools": server.get_tool_definitions()}
    
    elif method == "tools/call":
        tool_name = data.get("params", {}).get("name")
        arguments = data.get("params", {}).get("arguments", {})
        result = server.call_tool(tool_name, arguments)
        return {"content": [{"type": "text", "text": json.dumps(result)}]}
    
    return {"error": "Unknown method"}
```

---

## 9. Installation & Setup

### 9.1 Installation

```bash
# Prerequisites
bench get-app frappe
bench get-app erpnext
bench get-app pim  # Your PIM app

# Install INT
bench get-app https://github.com/your-org/int.git
bench --site your-site.local install-app int

# Install Python dependencies
cd apps/int
pip install -r requirements.txt

# Install Node dependencies (for workflow builder UI)
cd int/public
npm install
npm run build
```

### 9.2 requirements.txt

```
# API Clients
openai>=1.0.0
anthropic>=0.25.0
google-generativeai>=0.5.0

# CrewAI
crewai>=0.30.0
crewai-tools>=0.2.0

# LangChain (optional, for advanced chains)
langchain>=0.2.0
langchain-openai>=0.1.0
langchain-google-genai>=0.0.5
langchain-anthropic>=0.1.0

# HTTP & Async
httpx>=0.27.0
aiohttp>=3.9.0
tenacity>=8.2.0

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Redis (for event bus)
redis>=5.0.0

# Rate Limiting
ratelimit>=2.2.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

### 9.3 hooks.py

```python
# int/hooks.py

app_name = "int"
app_title = "INT - Enterprise Integration Platform"
app_publisher = "Your Company"
app_description = "Enterprise-grade marketplace integration platform"
app_email = "hello@yourcompany.com"
app_license = "MIT"

# Apps required
required_apps = ["frappe", "erpnext", "pim"]

# Fixtures
fixtures = [
    {
        "dt": "INT Platform",
        "filters": [["is_standard", "=", 1]]
    }
]

# Scheduled Tasks
scheduler_events = {
    "cron": {
        # Every 5 minutes - sync enabled connectors
        "*/5 * * * *": [
            "int.tasks.sync.scheduled_sync"
        ],
        # Every hour - reconciliation
        "0 * * * *": [
            "int.tasks.sync.reconciliation_check"
        ],
        # Daily - cleanup old logs
        "0 2 * * *": [
            "int.tasks.maintenance.cleanup_old_logs"
        ]
    }
}

# Document Events
doc_events = {
    "Sales Order": {
        "on_submit": "int.events.handlers.on_sales_order_submit",
        "on_cancel": "int.events.handlers.on_sales_order_cancel"
    },
    "Stock Entry": {
        "on_submit": "int.events.handlers.on_stock_entry_submit"
    },
    "Item Price": {
        "after_insert": "int.events.handlers.on_price_change",
        "on_update": "int.events.handlers.on_price_change"
    }
}

# Jinja Environment
jinja = {
    "methods": [
        "int.utils.jinja_methods"
    ]
}

# Website
website_route_rules = [
    {"from_route": "/int/<path:app_path>", "to_route": "int"}
]

# Includes
app_include_js = "/assets/int/js/int.bundle.js"
app_include_css = "/assets/int/css/int.bundle.css"

# DocType JS
doctype_js = {
    "Item": "public/js/item.js",
    "Sales Order": "public/js/sales_order.js"
}

# Permissions
permission_query_conditions = {
    "INT Connector": "int.permissions.get_connector_permissions",
    "INT Order": "int.permissions.get_order_permissions"
}

# Boot Session
boot_session = "int.startup.boot_session"

# Background Jobs
background_jobs = [
    {
        "method": "int.events.worker.start_event_worker",
        "queue": "long",
        "timeout": 86400  # 24 hours
    }
]
```

---

## 10. Testing Strategy

### 10.1 Test Structure

```
int/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_connectors/
│   │   ├── test_base_connector.py
│   │   ├── test_trendyol.py
│   │   ├── test_hepsiburada.py
│   │   └── test_amazon.py
│   ├── test_ai/
│   │   ├── test_router.py
│   │   ├── test_product_matcher.py
│   │   └── test_nl_config.py
│   ├── test_events/
│   │   ├── test_event_bus.py
│   │   └── test_handlers.py
│   ├── test_workflows/
│   │   └── test_engine.py
│   └── test_api/
│       ├── test_rest_api.py
│       └── test_webhooks.py
```

### 10.2 Sample Test

```python
# int/tests/test_ai/test_product_matcher.py

import pytest
import frappe
from int.ai.agents.product_matcher import ProductMatcherAgent


class TestProductMatcher:
    
    @pytest.fixture
    def agent(self):
        return ProductMatcherAgent()
    
    @pytest.fixture
    def source_product(self):
        return {
            "title": "Nike Air Max 90 Erkek Spor Ayakkabı Siyah",
            "brand": "Nike",
            "category": "Ayakkabı > Spor Ayakkabı",
            "sku": "NIKE-AM90-BLK-42",
            "barcode": "8690000123456",
            "attributes": {
                "color": "Siyah",
                "size": "42",
                "material": "Deri/Tekstil"
            }
        }
    
    @pytest.fixture
    def target_products(self):
        return [
            {
                "title": "Nike Air Max 90 Erkek Ayakkabı",
                "brand": "Nike",
                "barcode": "8690000123456",  # Same barcode
                "attributes": {"Renk": "Siyah", "Numara": "42"}
            },
            {
                "title": "Adidas Ultraboost Erkek Koşu Ayakkabısı",
                "brand": "Adidas",
                "barcode": "8690000789012",
                "attributes": {"Renk": "Siyah", "Numara": "42"}
            },
            {
                "title": "Nike Air Max 90 Kadın Ayakkabı Beyaz",
                "brand": "Nike",
                "barcode": "8690000123457",  # Different variant
                "attributes": {"Renk": "Beyaz", "Numara": "38"}
            }
        ]
    
    def test_exact_barcode_match(self, agent, source_product, target_products):
        """Test that exact barcode match returns high confidence"""
        matches = agent.match_products(source_product, target_products)
        
        assert len(matches) >= 1
        best_match = matches[0]
        assert best_match[1] >= 0.99  # Confidence
        assert best_match[2] == "exact"  # Match type
        assert best_match[0]["barcode"] == source_product["barcode"]
    
    def test_different_brand_no_match(self, agent, source_product, target_products):
        """Test that different brand products don't match"""
        matches = agent.match_products(source_product, target_products)
        
        # Adidas product should not be in matches
        for match in matches:
            assert match[0]["brand"] != "Adidas"
    
    def test_variant_detection(self, agent, source_product, target_products):
        """Test that variants are detected correctly"""
        # Remove exact match to test variant detection
        target_products_no_exact = [p for p in target_products 
                                    if p["barcode"] != source_product["barcode"]]
        
        matches = agent.match_products(source_product, target_products_no_exact,
                                       min_confidence=0.5)
        
        # Should find the white Nike variant
        variant_matches = [m for m in matches if m[2] == "variant"]
        assert len(variant_matches) >= 0  # May or may not detect variant
    
    @pytest.mark.integration
    def test_ai_matching_integration(self, agent, source_product, target_products):
        """Integration test for AI-powered matching"""
        # This test makes actual API calls
        matches = agent.match_products(source_product, target_products[:2])
        
        assert len(matches) >= 1
        # Verify AI task was logged
        task = frappe.get_last_doc("INT AI Task", 
                                   filters={"task_type": "Product_Matching"})
        assert task is not None
        assert task.status == "Completed"
```

---

## 11. Deployment

### 11.1 Production Checklist

```markdown
## Pre-deployment Checklist

### Security
- [ ] All API keys stored in encrypted fields
- [ ] Webhook secrets generated and configured
- [ ] Rate limiting configured for all connectors
- [ ] HTTPS enabled
- [ ] CORS configured properly
- [ ] Input validation on all endpoints

### Performance
- [ ] Redis configured for event bus
- [ ] Background workers scaled appropriately
- [ ] Database indexes created
- [ ] Query optimization verified
- [ ] CDN configured for static assets

### Monitoring
- [ ] Error logging configured (Sentry/equivalent)
- [ ] Sync metrics dashboard created
- [ ] Alert rules configured
- [ ] Uptime monitoring enabled

### Compliance
- [ ] KVKK compliance verified
- [ ] Data retention policies implemented
- [ ] Audit logging enabled
- [ ] User consent flows implemented

### Backup
- [ ] Database backup schedule configured
- [ ] File backup for attachments
- [ ] Disaster recovery plan documented
```

### 11.2 Docker Compose (Production)

```yaml
# docker-compose.prod.yml
version: "3.8"

services:
  frappe:
    image: frappe/erpnext:v15
    volumes:
      - sites:/home/frappe/frappe-bench/sites
      - logs:/home/frappe/frappe-bench/logs
    environment:
      - FRAPPE_SITE=your-site.com
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '2'
          memory: 4G

  worker-short:
    image: frappe/erpnext:v15
    command: bench worker --queue short
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    deploy:
      replicas: 2

  worker-long:
    image: frappe/erpnext:v15
    command: bench worker --queue long
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    deploy:
      replicas: 4

  event-worker:
    image: frappe/erpnext:v15
    command: bench execute int.events.worker.start_event_worker
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    deploy:
      replicas: 2

  scheduler:
    image: frappe/erpnext:v15
    command: bench schedule
    volumes:
      - sites:/home/frappe/frappe-bench/sites

  redis-cache:
    image: redis:7-alpine
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

  redis-queue:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-queue:/data

  mariadb:
    image: mariadb:10.6
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
    volumes:
      - mariadb:/var/lib/mysql
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

volumes:
  sites:
  logs:
  redis-queue:
  mariadb:
```

---

## 12. Roadmap

### Phase 1: MVP (8 weeks)
- Core DocTypes
- Trendyol connector
- Basic sync functionality
- Simple workflow engine
- REST API

### Phase 2: AI Integration (6 weeks)
- Multi-LLM router
- Product matching agent
- Natural language configuration
- CrewAI integration

### Phase 3: Enterprise Features (8 weeks)
- SOC 2 compliance features
- Advanced RBAC
- Audit logging
- SLA monitoring
- White-label support

### Phase 4: Global Expansion (6 weeks)
- Amazon global connectors
- eBay connector
- Multi-currency support
- GDPR compliance tools

### Phase 5: Advanced AI (Ongoing)
- Demand forecasting
- Dynamic pricing
- Anomaly detection
- Conversational interface

---

## Appendix A: Frappe AI Repositories Reference

| Repository | Purpose | Integration |
|------------|---------|-------------|
| [KorucuTech/kai](https://github.com/KorucuTech/kai) | CrewAI integration | Native |
| [erpnextai/next_ai](https://github.com/erpnextai/next_ai) | Content generation | Optional |
| [buildswithpaul/Frappe_Assistant_Core](https://github.com/buildswithpaul/Frappe_Assistant_Core) | MCP support | Native |
| [manavmandli/frappe_openai_integration](https://github.com/manavmandli/frappe_openai_integration) | OpenAI integration | Reference |
| [ERPGulf/changAI](https://github.com/ERPGulf/changAI) | AI for ERPNext | Reference |

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Author**: INT Team
