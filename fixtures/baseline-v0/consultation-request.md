# Synthetic consultation request

## Goal

Choose a safe retry strategy for a background synchronization worker.

## Current state

The normal executor has already implemented the worker and verified the happy path.

## Decision needed

Should retries use a fixed interval or exponential backoff?

## Constraints

- the remote service rate-limits bursts;
- synchronization is not latency-critical;
- duplicated writes must remain idempotent;
- the existing implementation should stay simple.

## Attempted / evidence

- fixed 1-second retry caused a synthetic rate-limit failure in a local test;
- no production data is included in this fixture.

## Question

Give a short second opinion on the retry policy. Do not implement code or start a broader architecture review.
