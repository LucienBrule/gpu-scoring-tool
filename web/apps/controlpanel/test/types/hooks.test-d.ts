import { expectType } from 'tsd';
import { useValidateArtifact, UseValidateArtifactResult, ArtifactValidationOptions } from '../../src/hooks/useValidateArtifact';
import { usePersistListings, UsePersistListingsResult, PersistListingsOptions } from '../../src/hooks/usePersistListings';
import { useHealth } from '../../src/hooks/useHealth';
import { useGpuListings, UseGpuListingsParams, UseGpuListingsResult } from '../../src/hooks/useGpuListings';
import { ArtifactValidationResult, ImportResult, HealthStatus, GpuListing } from '@repo/client';
import { UseQueryResult } from '@tanstack/react-query';

// Test useValidateArtifact hook return type
expectType<
  (options?: ArtifactValidationOptions) => UseValidateArtifactResult
>(useValidateArtifact);

// Test the return type structure of useValidateArtifact
type ValidateArtifactReturnType = ReturnType<typeof useValidateArtifact>;
expectType<{
  validateFile: (file: File) => void;
  data: ArtifactValidationResult | undefined;
  isLoading: boolean;
  isError: boolean;
  error: Error | null;
  isSuccess: boolean;
  progress: number;
  validationError: string | null;
  reset: () => void;
}>({} as ValidateArtifactReturnType);

// Test usePersistListings hook return type
expectType<
  (options?: PersistListingsOptions) => UsePersistListingsResult
>(usePersistListings);

// Test the return type structure of usePersistListings
type PersistListingsReturnType = ReturnType<typeof usePersistListings>;
expectType<{
  persistListings: (params: { listings: GpuListing[] }) => void;
  data: ImportResult | undefined;
  isLoading: boolean;
  isError: boolean;
  error: Error | null;
  isSuccess: boolean;
  validationError: string | null;
  reset: () => void;
}>({}  as PersistListingsReturnType);

// Test useHealth hook return type
expectType<
  () => UseQueryResult<HealthStatus, Error>
>(useHealth);

// Test the return type structure of useHealth
type HealthReturnType = ReturnType<typeof useHealth>;
expectType<UseQueryResult<HealthStatus, Error>>({} as HealthReturnType);

// Test useGpuListings hook return type
expectType<
  (options?: UseGpuListingsParams) => UseGpuListingsResult
>(useGpuListings);

// Test the return type structure of useGpuListings
type GpuListingsReturnType = ReturnType<typeof useGpuListings>;
expectType<UseGpuListingsResult>({} as GpuListingsReturnType);