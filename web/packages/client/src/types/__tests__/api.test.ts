/**
 * Tests for domain-aligned type aliases
 * 
 * This file verifies that the type aliases in api.ts correctly resolve to the
 * generated DTO types from the OpenAPI generator.
 */

import {
  ArtifactValidationResult,
  GpuListing,
  GpuModel,
  GpuReport,
  HttpValidationError,
  HealthStatus,
  ImportResult,
  ImportSummaryStats,
  MlPredictionRequest,
  MlPredictionResponse,
  PipelineImportRequest,
  ApiValidationError,
  RowError,
  SchemaVersion,
  SchemaVersionInfo,
  ValidationErrorLocation,
  GpuReportRow
} from '../api';

import type {
  ArtifactValidationResultDTO,
  GPUListingDTO,
  GPUModelDTO,
  HTTPValidationError as HTTPValidationErrorDTO,
  HealthStatus as HealthStatusDTO,
  ImportResultDTO,
  ImportSummaryStatsDTO,
  MLPredictionRequest as MLPredictionRequestDTO,
  MLPredictionResponse as MLPredictionResponseDTO,
  PipelineImportRequestDTO,
  ReportDTO,
  RowErrorDTO,
  SchemaVersion as SchemaVersionDTO,
  SchemaVersionInfo as SchemaVersionInfoDTO,
  ValidationError,
  ValidationErrorLocInner
} from '@repo/client-generated';

// Type compatibility tests
// These tests verify that our domain-aligned type aliases are compatible with
// the original DTO types from the OpenAPI generator.

describe('Domain-aligned type aliases', () => {
  it('GpuListing should be compatible with GPUListingDTO', () => {
    // TypeScript will error if these types are not compatible
    const assertType = (value: GpuListing): GPUListingDTO => value;
    const reverseAssertType = (value: GPUListingDTO): GpuListing => value;
    
    // This is just to make TypeScript happy - the test is purely at compile time
    expect(typeof assertType).toBe('function');
    expect(typeof reverseAssertType).toBe('function');
  });

  it('GpuModel should be compatible with GPUModelDTO', () => {
    const assertType = (value: GpuModel): GPUModelDTO => value;
    const reverseAssertType = (value: GPUModelDTO): GpuModel => value;
    
    expect(typeof assertType).toBe('function');
    expect(typeof reverseAssertType).toBe('function');
  });

  it('GpuReport should be compatible with ReportDTO', () => {
    const assertType = (value: GpuReport): ReportDTO => value;
    const reverseAssertType = (value: ReportDTO): GpuReport => value;
    
    expect(typeof assertType).toBe('function');
    expect(typeof reverseAssertType).toBe('function');
  });

  it('GpuReportRow should be compatible with GPUListingDTO', () => {
    const assertType = (value: GpuReportRow): GPUListingDTO => value;
    const reverseAssertType = (value: GPUListingDTO): GpuReportRow => value;
    
    expect(typeof assertType).toBe('function');
    expect(typeof reverseAssertType).toBe('function');
  });
});