"use client";

import React from "react";
import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@repo/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@repo/ui/card";
import { Button } from "@repo/ui/button";
import { Input } from "@repo/ui/input";
import { Label } from "@repo/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@repo/ui/select";
import { Alert, AlertDescription, AlertTitle } from "@repo/ui/alert";
import { Checkbox } from "@repo/ui/checkbox";
import { useDropzone } from "react-dropzone";
import { useImportCsv } from "@/hooks/useImportCsv";
import { useImportFromPipeline, ImportMode, ImportStatus } from "@/hooks/useImportFromPipeline";
import { useValidateArtifact } from "@/hooks/useValidateArtifact";
import { AlertCircle, CheckCircle, Upload, FileText, Database, FileCheck, Loader2 } from "lucide-react";
import { ProgressBar } from "@/components/ui/ProgressBar";

export default function ImportToolsPage() {
  // Tab state
  const [activeTab, setActiveTab] = useState("csv");

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Import Tools</h1>
      
      <Tabs defaultValue="csv" value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid grid-cols-3 mb-6">
          <TabsTrigger value="csv" className="flex items-center gap-2">
            <FileText className="h-4 w-4" />
            <span>CSV Import</span>
          </TabsTrigger>
          <TabsTrigger value="pipeline" className="flex items-center gap-2">
            <Database className="h-4 w-4" />
            <span>Pipeline Import</span>
          </TabsTrigger>
          <TabsTrigger value="validate" className="flex items-center gap-2">
            <FileCheck className="h-4 w-4" />
            <span>Artifact Validation</span>
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="csv">
          <CsvImportSection />
        </TabsContent>
        
        <TabsContent value="pipeline">
          <PipelineImportSection />
        </TabsContent>
        
        <TabsContent value="validate">
          <ArtifactValidationSection />
        </TabsContent>
      </Tabs>
    </div>
  );
}

// CSV Import Section
function CsvImportSection() {
  const [file, setFile] = useState<File | null>(null);
  const [columnMapping, setColumnMapping] = useState({
    title: true,
    price: true,
    model: true,
    url: true,
    description: true,
  });
  
  const { 
    importFile, 
    data: importResult, 
    isLoading, 
    isError, 
    error, 
    isSuccess, 
    progress, 
    validationError,
    reset 
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
  
  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
      }
    },
  });
  
  const handleImport = () => {
    if (file) {
      importFile(file);
    }
  };
  
  const handleReset = () => {
    setFile(null);
    reset();
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>CSV Import</CardTitle>
        <CardDescription>
          Import GPU listings from a CSV file. The file should contain columns for title, price, model, and other relevant data.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {!isSuccess && (
          <>
            <div 
              {...getRootProps()} 
              className={`border-2 border-dashed rounded-lg p-6 mb-4 text-center cursor-pointer transition-colors ${
              isDragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-700'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-2" />
              {isDragActive ? (
                <p>Drop the CSV file here...</p>
              ) : (
                <div>
                  <p className="mb-1">Drag and drop a CSV file here, or click to select a file</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Maximum file size: 10MB
                  </p>
                </div>
              )}
            </div>
            
            {file && (
              <div className="mb-4 p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <p className="font-medium">Selected file:</p>
                <p className="text-sm">{file.name} ({(file.size / 1024).toFixed(2)} KB)</p>
              </div>
            )}
            
            <div className="mb-6">
              <h3 className="text-lg font-medium mb-2">Column Mapping</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                Select which columns to import from your CSV file.
              </p>
              
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(columnMapping).map(([column, isEnabled]) => (
                  <div key={column} className="flex items-center space-x-2">
                    <Checkbox 
                      id={`column-${column}`} 
                      checked={isEnabled}
                      onCheckedChange={(checked) => {
                        setColumnMapping({
                          ...columnMapping,
                          [column]: !!checked
                        });
                      }}
                    />
                    <Label htmlFor={`column-${column}`} className="capitalize">
                      {column}
                    </Label>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="flex space-x-2">
              <Button 
                onClick={handleImport} 
                disabled={!file || isLoading}
                className="flex items-center gap-2"
              >
                {isLoading ? 'Importing...' : 'Import CSV'}
              </Button>
              <Button 
                variant="outline" 
                onClick={handleReset}
                disabled={isLoading}
              >
                Reset
              </Button>
            </div>
            
            {validationError && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{validationError}</AlertDescription>
              </Alert>
            )}
            
            {isLoading && (
              <div className="mt-4">
                <p className="mb-2">Uploading... {progress}%</p>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                  <div 
                    className="bg-blue-600 h-2.5 rounded-full" 
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            )}
            
            {isError && error && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Import Failed</AlertTitle>
                <AlertDescription>{error.message}</AlertDescription>
              </Alert>
            )}
          </>
        )}
        
        {isSuccess && importResult && (
          <div className="space-y-4">
            <Alert className="bg-green-50 dark:bg-green-900/20 border-green-500">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <AlertTitle>Import Successful</AlertTitle>
              <AlertDescription>
                Successfully imported data from CSV file.
              </AlertDescription>
            </Alert>
            
            <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Records Imported</p>
                <p className="text-xl font-semibold">{importResult.recordCount || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Errors</p>
                <p className="text-xl font-semibold">{importResult.errorCount || 0}</p>
              </div>
              {importResult.firstModel && (
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">First Model</p>
                  <p className="font-medium">{importResult.firstModel}</p>
                </div>
              )}
              {importResult.lastModel && (
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Last Model</p>
                  <p className="font-medium">{importResult.lastModel}</p>
                </div>
              )}
            </div>
            
            <Button onClick={handleReset}>Import Another File</Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Pipeline Import Section
function PipelineImportSection() {
  const [formData, setFormData] = useState({
    inputCsvPath: '',
    sourceLabel: '',
    campaignId: '',
    startDate: '',
    endDate: '',
  });
  const [importMode, setImportMode] = useState<ImportMode>(ImportMode.APPEND);
  const [metadata, setMetadata] = useState<Record<string, string>>({});
  const [metadataKey, setMetadataKey] = useState('');
  const [metadataValue, setMetadataValue] = useState('');
  const [enablePolling, setEnablePolling] = useState(true);
  
  const { 
    importFromPipeline, 
    data: importResult, 
    isLoading, 
    isError, 
    error, 
    isSuccess, 
    validationError,
    status,
    isPolling,
    pollingAttempt,
    maxPollingAttempts,
    reset 
  } = useImportFromPipeline({
    onSuccess: (data) => {
      console.log('Pipeline import successful:', data);
    },
    onError: (error) => {
      console.error('Pipeline import failed:', error);
    },
    enablePolling: enablePolling,
    pollingInterval: 3000,
    maxPollingAttempts: 20
  });
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleAddMetadata = () => {
    if (metadataKey && metadataValue) {
      setMetadata({
        ...metadata,
        [metadataKey]: metadataValue
      });
      setMetadataKey('');
      setMetadataValue('');
    }
  };
  
  const handleRemoveMetadata = (key: string) => {
    const newMetadata = { ...metadata };
    delete newMetadata[key];
    setMetadata(newMetadata);
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    importFromPipeline({
      inputCsvPath: formData.inputCsvPath,
      sourceLabel: formData.sourceLabel,
      campaignId: formData.campaignId || undefined,
      metadata: Object.keys(metadata).length > 0 ? metadata : undefined,
      importMode: importMode,
      startDate: formData.startDate || undefined,
      endDate: formData.endDate || undefined
    });
  };
  
  const handleReset = () => {
    setFormData({
      inputCsvPath: '',
      sourceLabel: '',
      campaignId: '',
      startDate: '',
      endDate: '',
    });
    setImportMode(ImportMode.APPEND);
    setEnablePolling(true);
    setMetadata({});
    reset();
  };
  
  return (
    <Card title={""}  href={""}>
      <CardHeader>
        <CardTitle>Pipeline Import</CardTitle>
        <CardDescription>
          Import data from the glyphsieve pipeline. Specify the path to the pipeline output file and additional metadata.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {!isSuccess && (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="inputCsvPath">Input CSV Path</Label>
              <Input
                id="inputCsvPath"
                name="inputCsvPath"
                value={formData.inputCsvPath}
                onChange={handleInputChange}
                placeholder="/path/to/pipeline/output.csv"
                required
              />
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Full path to the pipeline output file on the server
              </p>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="sourceLabel">Source Label</Label>
              <Input
                id="sourceLabel"
                name="sourceLabel"
                value={formData.sourceLabel}
                onChange={handleInputChange}
                placeholder="Pipeline Import August 2025"
                required
              />
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Human-readable tag for this data source
              </p>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="campaignId">Campaign ID (Optional)</Label>
              <Input
                id="campaignId"
                name="campaignId"
                value={formData.campaignId}
                onChange={handleInputChange}
                placeholder="campaign-123"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="importMode">Import Mode</Label>
              <Select 
                value={importMode} 
                onValueChange={(value) => setImportMode(value as ImportMode)}
              >
                <SelectTrigger id="importMode">
                  <SelectValue placeholder="Select import mode" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ImportMode.APPEND}>Append</SelectItem>
                  <SelectItem value={ImportMode.REPLACE}>Replace</SelectItem>
                  <SelectItem value={ImportMode.MERGE}>Merge</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                How to handle existing data
              </p>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="startDate">Start Date (Optional)</Label>
                <Input
                  id="startDate"
                  name="startDate"
                  type="date"
                  value={formData.startDate}
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="endDate">End Date (Optional)</Label>
                <Input
                  id="endDate"
                  name="endDate"
                  type="date"
                  value={formData.endDate}
                  onChange={handleInputChange}
                />
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox 
                id="enablePolling" 
                checked={enablePolling}
                onCheckedChange={(checked) => setEnablePolling(!!checked)}
              />
              <Label htmlFor="enablePolling">
                Enable status polling for long-running imports
              </Label>
            </div>
            
            <div className="space-y-2">
              <Label>Metadata (Optional)</Label>
              <div className="flex space-x-2">
                <Input
                  value={metadataKey}
                  onChange={(e) => setMetadataKey(e.target.value)}
                  placeholder="Key"
                  className="w-1/3"
                />
                <Input
                  value={metadataValue}
                  onChange={(e) => setMetadataValue(e.target.value)}
                  placeholder="Value"
                  className="w-1/3"
                />
                <Button 
                  type="button" 
                  onClick={handleAddMetadata}
                  disabled={!metadataKey || !metadataValue}
                  variant="outline"
                  className="w-1/3"
                >
                  Add Metadata
                </Button>
              </div>
              
              {Object.keys(metadata).length > 0 && (
                <div className="mt-2 p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                  <p className="font-medium mb-2">Current Metadata:</p>
                  <div className="space-y-2">
                    {Object.entries(metadata).map(([key, value]) => (
                      <div key={key} className="flex justify-between items-center">
                        <div>
                          <span className="font-medium">{key}:</span> {value}
                        </div>
                        <Button 
                          type="button" 
                          variant="ghost" 
                          size="sm"
                          onClick={() => handleRemoveMetadata(key)}
                        >
                          Remove
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <div className="flex space-x-2">
              <Button 
                type="submit" 
                disabled={isLoading || isPolling}
                className="flex items-center gap-2"
              >
                {isLoading ? 'Importing...' : 'Import from Pipeline'}
              </Button>
              <Button 
                type="button"
                variant="outline" 
                onClick={handleReset}
                disabled={isLoading || isPolling}
              >
                Reset
              </Button>
            </div>
            
            {/* Polling Status */}
            {isPolling && (
              <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-300 rounded-lg flex items-center">
                <Loader2 className="h-4 w-4 mr-2 animate-spin text-blue-500" />
                <div>
                  <p className="font-medium">Checking import status...</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Attempt {pollingAttempt} of {maxPollingAttempts}
                  </p>
                </div>
              </div>
            )}
            
            {/* Processing Status */}
            {!isPolling && status === ImportStatus.PROCESSING && (
              <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-300 rounded-lg">
                <p className="font-medium">Import is being processed...</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  This may take a few moments depending on the size of the dataset.
                </p>
              </div>
            )}
            
            {validationError && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{validationError}</AlertDescription>
              </Alert>
            )}
            
            {isError && error && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Import Failed</AlertTitle>
                <AlertDescription>{error.message}</AlertDescription>
              </Alert>
            )}
          </form>
        )}
        
        {isSuccess && importResult && (
          <div className="space-y-4">
            <Alert className="bg-green-50 dark:bg-green-900/20 border-green-500">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <AlertTitle>Import Successful</AlertTitle>
              <AlertDescription>
                Successfully imported data from the pipeline.
              </AlertDescription>
            </Alert>
            
            <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Records Imported</p>
                <p className="text-xl font-semibold">{importResult.recordCount || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Errors</p>
                <p className="text-xl font-semibold">{importResult.errorCount || 0}</p>
              </div>
              {importResult.firstModel && (
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">First Model</p>
                  <p className="font-medium">{importResult.firstModel}</p>
                </div>
              )}
              {importResult.lastModel && (
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Last Model</p>
                  <p className="font-medium">{importResult.lastModel}</p>
                </div>
              )}
            </div>
            
            <Button onClick={handleReset}>Import Another Dataset</Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Artifact Validation Section
function ArtifactValidationSection() {
  const [file, setFile] = useState<File | null>(null);
  const [saveToDisk, setSaveToDisk] = useState(false);
  const [schemaVersion, setSchemaVersion] = useState("latest");
  const [validationLevel, setValidationLevel] = useState("strict");
  
  const { 
    validateFile, 
    data: validationResult, 
    isLoading, 
    isError, 
    error, 
    isSuccess, 
    progress, 
    validationError,
    reset 
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
  
  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
      'application/json': ['.json'],
      'application/x-yaml': ['.yaml', '.yml'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
      }
    },
  });
  
  const handleValidate = () => {
    if (file) {
      validateFile(file);
    }
  };
  
  const handleReset = () => {
    setFile(null);
    reset();
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Artifact Validation</CardTitle>
        <CardDescription>
          Validate data artifacts (CSV, JSON, YAML) without importing them. This helps ensure data quality before ingestion.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {!isSuccess && (
          <>
            <div 
              {...getRootProps()} 
              className={`border-2 border-dashed rounded-lg p-6 mb-4 text-center cursor-pointer transition-colors ${
                isDragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-700'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-2" />
              {isDragActive ? (
                <p>Drop the file here...</p>
              ) : (
                <div>
                  <p className="mb-1">Drag and drop a file here, or click to select a file</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Supported formats: CSV, JSON, YAML (.csv, .json, .yaml, .yml)
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Maximum file size: 10MB
                  </p>
                </div>
              )}
            </div>
            
            {file && (
              <div className="mb-4 p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <p className="font-medium">Selected file:</p>
                <p className="text-sm">{file.name} ({(file.size / 1024).toFixed(2)} KB)</p>
              </div>
            )}
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="space-y-2">
                <Label htmlFor="schemaVersion">Schema Version</Label>
                <Select value={schemaVersion} onValueChange={setSchemaVersion}>
                  <SelectTrigger id="schemaVersion">
                    <SelectValue placeholder="Select schema version" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="latest">Latest</SelectItem>
                    <SelectItem value="1.0">1.0</SelectItem>
                    <SelectItem value="0.9">0.9</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="validationLevel">Validation Level</Label>
                <Select value={validationLevel} onValueChange={setValidationLevel}>
                  <SelectTrigger id="validationLevel">
                    <SelectValue placeholder="Select validation level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="strict">Strict</SelectItem>
                    <SelectItem value="lenient">Lenient</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            <div className="flex items-center space-x-2 mb-4">
              <Checkbox 
                id="saveToDisk" 
                checked={saveToDisk}
                onCheckedChange={(checked) => setSaveToDisk(checked)}
              />
              <Label htmlFor="saveToDisk">
                Save artifact to disk for debugging
              </Label>
            </div>
            
            <div className="flex space-x-2">
              <Button 
                onClick={handleValidate} 
                disabled={!file || isLoading}
                className="flex items-center gap-2"
              >
                {isLoading ? 'Validating...' : 'Validate Artifact'}
              </Button>
              <Button 
                variant="outline" 
                onClick={handleReset}
                disabled={isLoading}
              >
                Reset
              </Button>
            </div>
            
            {validationError && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{validationError}</AlertDescription>
              </Alert>
            )}
            
            {isLoading && (
              <div className="mt-4">
                <p className="mb-2">Uploading... {progress}%</p>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                  <div 
                    className="bg-blue-600 h-2.5 rounded-full" 
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            )}
            
            {isError && error && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Validation Failed</AlertTitle>
                <AlertDescription>{error.message}</AlertDescription>
              </Alert>
            )}
          </>
        )}
        
        {isSuccess && validationResult && (
          <div className="space-y-4">
            {validationResult.valid ? (
              <Alert className="bg-green-50 dark:bg-green-900/20 border-green-500">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <AlertTitle>Validation Successful</AlertTitle>
                <AlertDescription>
                  The artifact is valid and conforms to the schema.
                </AlertDescription>
              </Alert>
            ) : (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Validation Failed</AlertTitle>
                <AlertDescription>
                  The artifact does not conform to the schema.
                </AlertDescription>
              </Alert>
            )}
            
            <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Artifact Type</p>
                <p className="font-medium">{validationResult.type}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Schema Version</p>
                <p className="font-medium">{validationResult.schemaVersion}</p>
              </div>
              {validationResult.rows !== undefined && validationResult.rows !== null && (
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Rows</p>
                  <p className="font-medium">{validationResult.rows}</p>
                </div>
              )}
              {validationResult.fileSize !== undefined && validationResult.fileSize !== null && (
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">File Size</p>
                  <p className="font-medium">{(validationResult.fileSize / 1024).toFixed(2)} KB</p>
                </div>
              )}
              {validationResult.savedToDisk && validationResult.savedPath && (
                <div className="col-span-2">
                  <p className="text-sm text-gray-500 dark:text-gray-400">Saved Path</p>
                  <p className="font-medium break-all">{validationResult.savedPath}</p>
                </div>
              )}
            </div>
            
            {validationResult.warnings && validationResult.warnings.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Warnings</h3>
                <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-300 rounded-lg">
                  <ul className="list-disc pl-5 space-y-1">
                    {validationResult.warnings.map((warning, index) => (
                      <li key={index} className="text-sm">{warning}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
            
            {validationResult.errors && validationResult.errors.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Errors</h3>
                <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-300 rounded-lg">
                  <ul className="list-disc pl-5 space-y-1">
                    {validationResult.errors.map((error, index) => (
                      <li key={index} className="text-sm">{error}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
            
            <Button onClick={handleReset}>Validate Another File</Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}