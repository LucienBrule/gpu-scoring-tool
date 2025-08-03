"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@repo/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@repo/ui/card";
import { Button } from "@repo/ui/button";
import { Input } from "@repo/ui/input";
import { Label } from "@repo/ui/label";
import { Alert, AlertDescription, AlertTitle } from "@repo/ui/alert";
import { Checkbox } from "@repo/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@repo/ui/select";
import { AlertCircle, CheckCircle, Upload, FileText, Database, FileCheck } from "lucide-react";
import { Spinner } from "../../components/ui/Spinner";

// Import hooks
import { useHealth } from "../../hooks/useHealth";
import { useGpuListings } from "../../hooks/useGpuListings";
import { useGpuModels } from "../../hooks/useGpuModels";
import { useGpuReports } from "../../hooks/useGpuReports";
import { useSchemaInfo } from "../../hooks/useSchemaInfo";
import { useForecastDeltas } from "../../hooks/useForecastDeltas";
import { useImportCsv } from "../../hooks/useImportCsv";
import { useImportFromPipeline } from "../../hooks/useImportFromPipeline";
import { useValidateArtifact } from "../../hooks/useValidateArtifact";
import { useGpuClassification } from "../../hooks/useGpuClassification";

// Feature flag to hide in production
const isDevelopment = process.env.NODE_ENV === 'development';

// This component will only be rendered in development mode
export default function DevHarnessPage() {
  // Tab state - must be defined before conditional return to follow React Hooks rules
  const [activeTab, setActiveTab] = useState("health");
  
  // Redirect to home if not in development mode
  if (!isDevelopment) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Alert variant="destructive">
          <AlertTitle>Access Denied</AlertTitle>
          <AlertDescription>
            The Developer Harness is only available in development mode.
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Developer Harness</h1>
        <div className="text-sm text-gray-500 dark:text-gray-400">
          Environment: {process.env.NODE_ENV}
        </div>
      </div>

      <p className="mb-6 text-gray-600 dark:text-gray-300">
        This page allows you to test all hooks and endpoints in isolation. Use the tabs below to navigate between different categories of hooks.
      </p>
      
      <Tabs defaultValue="health" value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid grid-cols-5 mb-6">
          <TabsTrigger value="health">Health</TabsTrigger>
          <TabsTrigger value="data">Data Hooks</TabsTrigger>
          <TabsTrigger value="forecast">Forecast</TabsTrigger>
          <TabsTrigger value="import">Import</TabsTrigger>
          <TabsTrigger value="ml">ML</TabsTrigger>
        </TabsList>
        
        {/* Health Hooks */}
        <TabsContent value="health">
          <HealthSection />
        </TabsContent>
        
        {/* Data Hooks */}
        <TabsContent value="data">
          <DataSection />
        </TabsContent>
        
        {/* Forecast Hooks */}
        <TabsContent value="forecast">
          <ForecastSection />
        </TabsContent>
        
        {/* Import Hooks */}
        <TabsContent value="import">
          <ImportSection />
        </TabsContent>
        
        {/* ML Hooks */}
        <TabsContent value="ml">
          <MLSection />
        </TabsContent>
      </Tabs>
    </div>
  );
}

// Health Hooks Section
function HealthSection() {
  // Import the useHealth hook
  const { data: healthData, isLoading, isError, error, refetch } = useHealth();

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>useHealth / useHealthCheck</CardTitle>
          <CardDescription>
            Check the health status of the API
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Button 
              onClick={() => refetch()} 
              disabled={isLoading}
            >
              {isLoading ? 'Checking...' : 'Check Health'}
            </Button>
            
            {isLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Loading..." />
              </div>
            )}
            
            {isError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  {error?.message || 'An error occurred while fetching health status'}
                </AlertDescription>
              </Alert>
            )}
            
            {!isLoading && !isError && healthData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(healthData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Data Hooks Section
function DataSection() {
  // State for useGpuListings inputs
  const [listingsModel, setListingsModel] = useState("");
  const [listingsLimit, setListingsLimit] = useState("10");
  
  // useGpuListings hook
  const { 
    data: listingsData, 
    isLoading: listingsLoading, 
    isError: listingsError, 
    error: listingsErrorData,
    refetch: refetchListings
  } = useGpuListings({
    model: listingsModel || undefined,
    limit: listingsLimit ? parseInt(listingsLimit) : undefined
  });
  
  // useGpuModels hook
  const { 
    data: modelsData, 
    isLoading: modelsLoading, 
    isError: modelsError, 
    error: modelsErrorData,
    refetch: refetchModels
  } = useGpuModels();
  
  // useGpuReports hook
  const { 
    data: reportsData, 
    isLoading: reportsLoading, 
    isError: reportsError, 
    error: reportsErrorData,
    refetch: refetchReports
  } = useGpuReports();
  
  // useSchemaInfo hook
  const { 
    data: schemaData, 
    isLoading: schemaLoading, 
    isError: schemaError, 
    error: schemaErrorData,
    refetch: refetchSchema
  } = useSchemaInfo();
  
  // Handler for fetching listings
  const handleFetchListings = () => {
    refetchListings();
  };

  return (
    <div className="space-y-6">
      {/* useGpuListings / useListings */}
      <Card>
        <CardHeader>
          <CardTitle>useGpuListings / useListings</CardTitle>
          <CardDescription>
            Fetch GPU listings with optional filters
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="model">Model</Label>
                <Input 
                  id="model" 
                  placeholder="e.g., RTX 3080" 
                  value={listingsModel}
                  onChange={(e) => setListingsModel(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="limit">Limit</Label>
                <Input 
                  id="limit" 
                  type="number" 
                  value={listingsLimit}
                  onChange={(e) => setListingsLimit(e.target.value)}
                />
              </div>
            </div>
            
            <Button 
              onClick={handleFetchListings}
              disabled={listingsLoading}
            >
              {listingsLoading ? 'Fetching...' : 'Fetch Listings'}
            </Button>
            
            {listingsLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Loading..." />
              </div>
            )}
            
            {listingsError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  {listingsErrorData?.message || 'An error occurred while fetching listings'}
                </AlertDescription>
              </Alert>
            )}
            
            {!listingsLoading && !listingsError && listingsData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(listingsData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
      
      {/* useGpuModels / useModels */}
      <Card>
        <CardHeader>
          <CardTitle>useGpuModels / useModels</CardTitle>
          <CardDescription>
            Fetch GPU models
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Button 
              onClick={() => refetchModels()}
              disabled={modelsLoading}
            >
              {modelsLoading ? 'Fetching...' : 'Fetch Models'}
            </Button>
            
            {modelsLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Loading..." />
              </div>
            )}
            
            {modelsError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  {modelsErrorData?.message || 'An error occurred while fetching models'}
                </AlertDescription>
              </Alert>
            )}
            
            {!modelsLoading && !modelsError && modelsData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(modelsData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
      
      {/* useGpuReports / useReports */}
      <Card>
        <CardHeader>
          <CardTitle>useGpuReports / useReports</CardTitle>
          <CardDescription>
            Fetch GPU reports
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Button 
              onClick={() => refetchReports()}
              disabled={reportsLoading}
            >
              {reportsLoading ? 'Fetching...' : 'Fetch Reports'}
            </Button>
            
            {reportsLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Loading..." />
              </div>
            )}
            
            {reportsError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  {reportsErrorData?.message || 'An error occurred while fetching reports'}
                </AlertDescription>
              </Alert>
            )}
            
            {!reportsLoading && !reportsError && reportsData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(reportsData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
      
      {/* useSchemaInfo */}
      <Card>
        <CardHeader>
          <CardTitle>useSchemaInfo</CardTitle>
          <CardDescription>
            Fetch schema information
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Button 
              onClick={() => refetchSchema()}
              disabled={schemaLoading}
            >
              {schemaLoading ? 'Fetching...' : 'Fetch Schema Info'}
            </Button>
            
            {schemaLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Loading..." />
              </div>
            )}
            
            {schemaError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  {schemaErrorData?.message || 'An error occurred while fetching schema information'}
                </AlertDescription>
              </Alert>
            )}
            
            {!schemaLoading && !schemaError && schemaData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(schemaData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Forecast Hooks Section
function ForecastSection() {
  // State for useForecastDeltas inputs
  const [forecastModel, setForecastModel] = useState("");
  const [minPriceChangePct, setMinPriceChangePct] = useState("5");
  
  // useForecastDeltas hook
  const { 
    data: forecastData, 
    isLoading: forecastLoading, 
    isError: forecastError, 
    error: forecastErrorData,
    refetch: refetchForecast
  } = useForecastDeltas({
    model: forecastModel || undefined,
    minPriceChangePct: minPriceChangePct ? parseFloat(minPriceChangePct) : undefined
  });
  
  return (
    <div className="space-y-6">
      {/* useForecastDeltas */}
      <Card>
        <CardHeader>
          <CardTitle>useForecastDeltas</CardTitle>
          <CardDescription>
            Fetch forecast deltas with optional filters
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="forecastModel">Model</Label>
                <Input 
                  id="forecastModel" 
                  placeholder="e.g., RTX 3080" 
                  value={forecastModel}
                  onChange={(e) => setForecastModel(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="minPriceChangePct">Min Price Change %</Label>
                <Input 
                  id="minPriceChangePct" 
                  type="number" 
                  value={minPriceChangePct}
                  onChange={(e) => setMinPriceChangePct(e.target.value)}
                />
              </div>
            </div>
            
            <Button 
              onClick={() => refetchForecast()}
              disabled={forecastLoading}
            >
              {forecastLoading ? 'Fetching...' : 'Fetch Forecast Deltas'}
            </Button>
            
            {forecastLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Loading..." />
              </div>
            )}
            
            {forecastError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  {forecastErrorData?.message || 'An error occurred while fetching forecast deltas'}
                </AlertDescription>
              </Alert>
            )}
            
            {!forecastLoading && !forecastError && forecastData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(forecastData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Import Hooks Section
function ImportSection() {
  // State for useImportCsv
  const [csvFile, setCsvFile] = useState<File | null>(null);
  
  // useImportCsv hook
  const { 
    importFile, 
    data: importCsvData, 
    isLoading: importCsvLoading, 
    isError: importCsvError, 
    error: importCsvErrorData,
    progress: importCsvProgress,
    validationError: importCsvValidationError,
    reset: resetImportCsv
  } = useImportCsv({
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['.csv'],
    onSuccess: (data) => {
      console.log('Import successful:', data);
    },
    onError: (error) => {
      console.error('Import failed:', error);
    }
  });
  
  // State for useImportFromPipeline
  const [pipelineFormData, setPipelineFormData] = useState({
    inputCsvPath: '',
    sourceLabel: '',
    campaignId: '',
  });
  
  // useImportFromPipeline hook
  const { 
    importFromPipeline, 
    data: pipelineData, 
    isLoading: pipelineLoading, 
    isError: pipelineError, 
    error: pipelineErrorData,
    validationError: pipelineValidationError,
    reset: resetPipeline
  } = useImportFromPipeline({
    onSuccess: (data) => {
      console.log('Pipeline import successful:', data);
    },
    onError: (error) => {
      console.error('Pipeline import failed:', error);
    }
  });
  
  // Handle pipeline form input change
  const handlePipelineInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPipelineFormData({
      ...pipelineFormData,
      [name]: value
    });
  };
  
  // Handle pipeline import
  const handlePipelineImport = (e: React.FormEvent) => {
    e.preventDefault();
    importFromPipeline({
      inputCsvPath: pipelineFormData.inputCsvPath,
      sourceLabel: pipelineFormData.sourceLabel,
      campaignId: pipelineFormData.campaignId || undefined
    });
  };
  
  // Handle pipeline reset
  const handlePipelineReset = () => {
    setPipelineFormData({
      inputCsvPath: '',
      sourceLabel: '',
      campaignId: '',
    });
    resetPipeline();
  };
  
  // State for useValidateArtifact
  const [artifactFile, setArtifactFile] = useState<File | null>(null);
  const [saveToDisk, setSaveToDisk] = useState(false);
  
  // useValidateArtifact hook
  const { 
    validateFile, 
    data: artifactData, 
    isLoading: artifactLoading, 
    isError: artifactError, 
    error: artifactErrorData,
    progress: artifactProgress,
    validationError: artifactValidationError,
    reset: resetArtifact
  } = useValidateArtifact({
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['.csv', '.json', '.yaml', '.yml'],
    saveToDisk,
    onSuccess: (data) => {
      console.log('Validation successful:', data);
    },
    onError: (error) => {
      console.error('Validation failed:', error);
    }
  });
  
  // Handle artifact file selection
  const handleArtifactFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setArtifactFile(e.target.files[0]);
    }
  };
  
  // Handle artifact validation
  const handleValidateArtifact = () => {
    if (artifactFile) {
      validateFile(artifactFile);
    }
  };
  
  // Handle artifact reset
  const handleResetArtifact = () => {
    setArtifactFile(null);
    setSaveToDisk(false);
    resetArtifact();
  };
  
  // Handle file selection
  const handleCsvFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setCsvFile(e.target.files[0]);
    }
  };
  
  // Handle import
  const handleImportCsv = () => {
    if (csvFile) {
      importFile(csvFile);
    }
  };
  
  // Handle reset
  const handleResetCsv = () => {
    setCsvFile(null);
    resetImportCsv();
  };
  
  return (
    <div className="space-y-6">
      {/* useImportCsv */}
      <Card>
        <CardHeader>
          <CardTitle>useImportCsv</CardTitle>
          <CardDescription>
            Import data from a CSV file
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="csvFile">CSV File</Label>
              <Input 
                id="csvFile" 
                type="file" 
                accept=".csv" 
                onChange={handleCsvFileChange}
                disabled={importCsvLoading}
              />
            </div>
            
            {csvFile && (
              <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <p className="font-medium">Selected file:</p>
                <p className="text-sm">{csvFile.name} ({(csvFile.size / 1024).toFixed(2)} KB)</p>
              </div>
            )}
            
            <div className="flex space-x-2">
              <Button 
                onClick={handleImportCsv} 
                disabled={!csvFile || importCsvLoading}
              >
                {importCsvLoading ? 'Importing...' : 'Import CSV'}
              </Button>
              
              <Button 
                variant="outline" 
                onClick={handleResetCsv}
                disabled={importCsvLoading}
              >
                Reset
              </Button>
            </div>
            
            {importCsvValidationError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Validation Error</AlertTitle>
                <AlertDescription>{importCsvValidationError}</AlertDescription>
              </Alert>
            )}
            
            {importCsvLoading && (
              <div className="space-y-2">
                <p className="text-sm">Uploading... {importCsvProgress}%</p>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                  <div 
                    className="bg-blue-600 h-2.5 rounded-full" 
                    style={{ width: `${importCsvProgress}%` }}
                  ></div>
                </div>
              </div>
            )}
            
            {importCsvError && importCsvErrorData && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Import Failed</AlertTitle>
                <AlertDescription>{importCsvErrorData.message}</AlertDescription>
              </Alert>
            )}
            
            {!importCsvLoading && !importCsvError && importCsvData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(importCsvData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
      
      {/* useImportFromPipeline */}
      <Card>
        <CardHeader>
          <CardTitle>useImportFromPipeline</CardTitle>
          <CardDescription>
            Import data from the pipeline
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handlePipelineImport} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="inputCsvPath">Input CSV Path</Label>
                <Input 
                  id="inputCsvPath"
                  name="inputCsvPath"
                  placeholder="/path/to/file.csv"
                  value={pipelineFormData.inputCsvPath}
                  onChange={handlePipelineInputChange}
                  disabled={pipelineLoading}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="sourceLabel">Source Label</Label>
                <Input 
                  id="sourceLabel"
                  name="sourceLabel"
                  placeholder="Pipeline Import"
                  value={pipelineFormData.sourceLabel}
                  onChange={handlePipelineInputChange}
                  disabled={pipelineLoading}
                  required
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="campaignId">Campaign ID (Optional)</Label>
              <Input 
                id="campaignId"
                name="campaignId"
                placeholder="campaign-123"
                value={pipelineFormData.campaignId}
                onChange={handlePipelineInputChange}
                disabled={pipelineLoading}
              />
            </div>
            
            <div className="flex space-x-2">
              <Button 
                type="submit" 
                disabled={pipelineLoading}
              >
                {pipelineLoading ? 'Importing...' : 'Import from Pipeline'}
              </Button>
              
              <Button 
                type="button"
                variant="outline" 
                onClick={handlePipelineReset}
                disabled={pipelineLoading}
              >
                Reset
              </Button>
            </div>
            
            {pipelineValidationError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Validation Error</AlertTitle>
                <AlertDescription>{pipelineValidationError}</AlertDescription>
              </Alert>
            )}
            
            {pipelineLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Importing..." />
              </div>
            )}
            
            {pipelineError && pipelineErrorData && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Import Failed</AlertTitle>
                <AlertDescription>{pipelineErrorData.message}</AlertDescription>
              </Alert>
            )}
            
            {!pipelineLoading && !pipelineError && pipelineData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(pipelineData, null, 2)}
                </pre>
              </div>
            )}
          </form>
        </CardContent>
      </Card>
      
      {/* useValidateArtifact */}
      <Card>
        <CardHeader>
          <CardTitle>useValidateArtifact</CardTitle>
          <CardDescription>
            Validate a data artifact
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="artifactFile">Artifact File</Label>
              <Input 
                id="artifactFile" 
                type="file" 
                accept=".csv,.json,.yaml,.yml" 
                onChange={handleArtifactFileChange}
                disabled={artifactLoading}
              />
            </div>
            
            {artifactFile && (
              <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <p className="font-medium">Selected file:</p>
                <p className="text-sm">{artifactFile.name} ({(artifactFile.size / 1024).toFixed(2)} KB)</p>
              </div>
            )}
            
            <div className="flex items-center space-x-2">
              <Checkbox 
                id="saveToDisk" 
                checked={saveToDisk}
                onCheckedChange={(checked) => setSaveToDisk(!!checked)}
                disabled={artifactLoading}
              />
              <Label htmlFor="saveToDisk">Save to disk</Label>
            </div>
            
            <div className="flex space-x-2">
              <Button 
                onClick={handleValidateArtifact} 
                disabled={!artifactFile || artifactLoading}
              >
                {artifactLoading ? 'Validating...' : 'Validate Artifact'}
              </Button>
              
              <Button 
                variant="outline" 
                onClick={handleResetArtifact}
                disabled={artifactLoading}
              >
                Reset
              </Button>
            </div>
            
            {artifactValidationError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Validation Error</AlertTitle>
                <AlertDescription>{artifactValidationError}</AlertDescription>
              </Alert>
            )}
            
            {artifactLoading && (
              <div className="space-y-2">
                <p className="text-sm">Uploading... {artifactProgress}%</p>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                  <div 
                    className="bg-blue-600 h-2.5 rounded-full" 
                    style={{ width: `${artifactProgress}%` }}
                  ></div>
                </div>
              </div>
            )}
            
            {artifactError && artifactErrorData && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Validation Failed</AlertTitle>
                <AlertDescription>{artifactErrorData.message}</AlertDescription>
              </Alert>
            )}
            
            {!artifactLoading && !artifactError && artifactData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(artifactData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// ML Hooks Section
function MLSection() {
  // State for useGpuClassification
  const [title, setTitle] = useState("");
  
  // useGpuClassification hook
  const { 
    classifyGpu, 
    data: classificationData, 
    isLoading: classificationLoading, 
    isError: classificationError, 
    error: classificationErrorData,
    reset: resetClassification
  } = useGpuClassification();
  
  // Handle title input change
  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
  };
  
  // Handle classification
  const handleClassify = () => {
    if (title.trim()) {
      classifyGpu(title);
    }
  };
  
  // Handle reset
  const handleResetClassification = () => {
    setTitle("");
    resetClassification();
  };
  
  return (
    <div className="space-y-6">
      {/* useGpuClassification */}
      <Card>
        <CardHeader>
          <CardTitle>useGpuClassification</CardTitle>
          <CardDescription>
            Classify whether a text description refers to a GPU
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Title</Label>
              <Input 
                id="title" 
                placeholder="Enter a product title to classify" 
                value={title}
                onChange={handleTitleChange}
                disabled={classificationLoading}
              />
            </div>
            
            <div className="flex space-x-2">
              <Button 
                onClick={handleClassify} 
                disabled={!title.trim() || classificationLoading}
              >
                {classificationLoading ? 'Classifying...' : 'Classify'}
              </Button>
              
              <Button 
                variant="outline" 
                onClick={handleResetClassification}
                disabled={classificationLoading}
              >
                Reset
              </Button>
            </div>
            
            {classificationLoading && (
              <div className="text-center p-4">
                <Spinner size="md" color="primary" showText text="Classifying..." />
              </div>
            )}
            
            {classificationError && classificationErrorData && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Classification Failed</AlertTitle>
                <AlertDescription>{classificationErrorData.message}</AlertDescription>
              </Alert>
            )}
            
            {!classificationLoading && !classificationError && classificationData && (
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(classificationData, null, 2)}
                </pre>
                
                {classificationData.isGpu !== undefined && (
                  <div className="mt-4 p-3 rounded-lg border text-center font-medium">
                    {classificationData.isGpu ? (
                      <div className="text-green-500 dark:text-green-400">
                        <CheckCircle className="h-6 w-6 mx-auto mb-2" />
                        This is a GPU
                      </div>
                    ) : (
                      <div className="text-red-500 dark:text-red-400">
                        <AlertCircle className="h-6 w-6 mx-auto mb-2" />
                        This is NOT a GPU
                      </div>
                    )}
                    {classificationData.confidence !== undefined && (
                      <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                        Confidence: {(classificationData.confidence * 100).toFixed(2)}%
                      </p>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}