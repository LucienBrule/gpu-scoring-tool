/**
 * Domain-aligned type aliases for API DTOs
 * 
 * This file provides clean, domain-friendly type aliases for the generated
 * OpenAPI DTOs. These aliases decouple the application code from the exact
 * generator output, making it easier to refactor if DTO names change.
 */

import type {
  ArtifactValidationResultDTO,
  GPUListingDTO,
  GPUModelDTO,
  HealthStatus as HealthStatusDTO,
  HTTPValidationError,
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

// GPU Listings and Models
export type GpuListing = GPUListingDTO;
export type GpuModel = GPUModelDTO;
export type GpuReport = ReportDTO;

// Health and Status
export type HealthStatus = HealthStatusDTO;

// ML and Classification
export type MlPredictionRequest = MLPredictionRequestDTO;
export type MlPredictionResponse = MLPredictionResponseDTO;

// Import and Validation
export type ArtifactValidationResult = ArtifactValidationResultDTO;
export type ImportResult = ImportResultDTO;
export type ImportSummaryStats = ImportSummaryStatsDTO;
export type PipelineImportRequest = PipelineImportRequestDTO;
export type RowError = RowErrorDTO;

// Schema and Versioning
export type SchemaVersion = SchemaVersionDTO;
export type SchemaVersionInfo = SchemaVersionInfoDTO;

// Error Types
export type ApiValidationError = ValidationError;
export type ValidationErrorLocation = ValidationErrorLocInner;
export type HttpValidationError = HTTPValidationError;

// Legacy alias for backward compatibility
export type GpuReportRow = GPUListingDTO;