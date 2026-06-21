---

#  Architecture Diagram
<img width="438" height="425" alt="image" src="https://github.com/user-attachments/assets/a87da986-d2d9-442f-8280-df044daf7d00" />


---





# 💳 Idempotency Layer for Payment Processing API

## 📌 Overview

This project implements a **payment processing API with an idempotency layer** to prevent duplicate transactions caused by network retries.

It ensures that each payment request is processed **exactly once**, even if the client retries multiple times due to timeouts or failures.

---

# 🚨 Problem Statement

Payment systems often face a critical issue:

> Clients retry requests due to network delays, causing duplicate charges.

This system solves that by introducing:

* Idempotency-Key validation
* Request deduplication
* Race condition protection
* Transaction audit logging

---

# 🏗️ Architecture

The system is built using a layered architecture:

### 1. API Layer (FastAPI)

Handles HTTP requests and input validation.

### 2. Concurrency Control Layer

Uses **per-Idempotency-Key locks** to prevent race conditions.

### 3. Idempotency Layer

Ensures:

* First request is processed
* Duplicate requests return cached result
* Conflicting payloads are rejected

### 4. Service Layer

Simulates payment processing (2-second delay).

### 5. Storage Layer (In-Memory)

Stores transaction data for:

* replay protection
* audit history

### 6. Audit Layer

Exposes transaction history via query endpoint.

---

# 🔐 Key Features

## ✅ Idempotency Protection

Prevents duplicate payment processing using `Idempotency-Key`.

## ✅ Race Condition Safety

Uses **thread locks per key** to ensure atomic execution.

## ✅ Payload Integrity Check

Rejects requests with same key but different payload.

## ✅ Transaction Audit Trail

Stores full transaction history with:

* timestamp
* status
* response
* payment details

## ✅ Cache Hit Optimization

Returns cached response instantly for duplicate requests.

---

# 📡 API Endpoints

---

## 🔹 POST /process-payment

### Headers

```
Idempotency-Key: unique-key
```

### Body

```json
{
  "amount": 100,
  "currency": "GHS"
}
```

---

### Response (First Request)

```json
{
  "message": "Charged 100 GHS",
  "status" : 200
}
```

---

### Response (Duplicate Request)

```json
{
  "message": "Charged 100 GHS"
}
```

Header:

```
X-Cache-Hit: true
```

---

### Response (Different Payload, Same Key)

```json
{
  "message": "Idempotency key already used for a different request body"
}
```

Status:

```
422 Unprocessable Entity
```

---

## 🔹 GET /transactions/{key}

### Description

Returns stored transaction for auditing.

### Response

```json
{
  "idempotency_key": "abc123",
  "amount": 100,
  "currency": "GHS",
  "status": "completed",
  "timestamp": "2026-06-20T10:30:00Z",
  "response": {
    "message": "Charged 100 GHS",
    "status" : 200
  }
}
```

---

# 🧠 Design Decisions

## 1. In-Memory Store

Used a Python dictionary for simplicity and speed.

## 2. Per-Key Locking

Ensures only one request per Idempotency-Key is processed at a time.

## 3. Transaction Model

Created a structured `Transaction` object to support auditing and traceability.

## 4. Simulated Payment Delay

Used `sleep(2)` to mimic external payment gateway latency.

---

# 💡 Developer Choice Feature

##  Transaction Audit API

An additional endpoint was added:

```
GET /transactions/{key}
```

### Why it matters:

* Enables auditability of payments
* Helps debugging failed transactions
* Provides transparency for financial operations
* Turns system into a lightweight ledger





# 🧪 How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

# 🧠 Summary

This system guarantees:

> Each payment is processed exactly once, even under retries or concurrent requests.

---


