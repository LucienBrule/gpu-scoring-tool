import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import ImportToolsPage from '../page';
import { createQueryClientWrapper } from '../../../test-utils/queryClientWrapper';

// Mock the components used in the Import Tools page
vi.mock('@repo/ui/tabs', () => ({
  Tabs: ({ children }: { children: React.ReactNode }) => <div data-testid="tabs">{children}</div>,
  TabsContent: ({ children }: { children: React.ReactNode }) => <div data-testid="tabs-content">{children}</div>,
  TabsList: ({ children }: { children: React.ReactNode }) => <div data-testid="tabs-list">{children}</div>,
  TabsTrigger: ({ children }: { children: React.ReactNode }) => <div data-testid="tabs-trigger">{children}</div>,
}));

vi.mock('@repo/ui/card', () => ({
  Card: ({ children }: { children: React.ReactNode }) => <div data-testid="card">{children}</div>,
  CardContent: ({ children }: { children: React.ReactNode }) => <div data-testid="card-content">{children}</div>,
  CardDescription: ({ children }: { children: React.ReactNode }) => <div data-testid="card-description">{children}</div>,
  CardHeader: ({ children }: { children: React.ReactNode }) => <div data-testid="card-header">{children}</div>,
  CardTitle: ({ children }: { children: React.ReactNode }) => <div data-testid="card-title">{children}</div>,
}));

vi.mock('@repo/ui/button', () => ({
  Button: ({ children }: { children: React.ReactNode }) => <button data-testid="button">{children}</button>,
}));

vi.mock('@repo/ui/input', () => ({
  Input: () => <input data-testid="input" />,
}));

vi.mock('@repo/ui/label', () => ({
  Label: ({ children }: { children: React.ReactNode }) => <label data-testid="label">{children}</label>,
}));

vi.mock('@repo/ui/select', () => ({
  Select: ({ children }: { children: React.ReactNode }) => <div data-testid="select">{children}</div>,
  SelectContent: ({ children }: { children: React.ReactNode }) => <div data-testid="select-content">{children}</div>,
  SelectItem: ({ children }: { children: React.ReactNode }) => <div data-testid="select-item">{children}</div>,
  SelectTrigger: ({ children }: { children: React.ReactNode }) => <div data-testid="select-trigger">{children}</div>,
  SelectValue: ({ children }: { children: React.ReactNode }) => <div data-testid="select-value">{children}</div>,
}));

vi.mock('@repo/ui/alert', () => ({
  Alert: ({ children }: { children: React.ReactNode }) => <div data-testid="alert">{children}</div>,
  AlertDescription: ({ children }: { children: React.ReactNode }) => <div data-testid="alert-description">{children}</div>,
  AlertTitle: ({ children }: { children: React.ReactNode }) => <div data-testid="alert-title">{children}</div>,
}));

vi.mock('@repo/ui/checkbox', () => ({
  Checkbox: () => <input type="checkbox" data-testid="checkbox" />,
}));

vi.mock('react-dropzone', () => ({
  useDropzone: () => ({
    getRootProps: () => ({}),
    getInputProps: () => ({}),
    isDragActive: false,
    acceptedFiles: [],
  }),
}));

vi.mock('../../hooks/useImportCsv', () => ({
  useImportCsv: () => ({
    importFile: vi.fn(),
    data: undefined,
    isLoading: false,
    isError: false,
    error: null,
    isSuccess: false,
    progress: 0,
    validationError: null,
    reset: vi.fn(),
  }),
}));

vi.mock('../../hooks/useImportFromPipeline', () => ({
  useImportFromPipeline: () => ({
    importFromPipeline: vi.fn(),
    data: undefined,
    isLoading: false,
    isError: false,
    error: null,
    isSuccess: false,
    validationError: null,
    reset: vi.fn(),
  }),
}));

vi.mock('../../hooks/useValidateArtifact', () => ({
  useValidateArtifact: () => ({
    validateFile: vi.fn(),
    data: undefined,
    isLoading: false,
    isError: false,
    error: null,
    isSuccess: false,
    progress: 0,
    validationError: null,
    reset: vi.fn(),
  }),
}));

vi.mock('lucide-react', () => ({
  AlertCircle: () => <span data-testid="icon-alert-circle" />,
  CheckCircle: () => <span data-testid="icon-check-circle" />,
  Upload: () => <span data-testid="icon-upload" />,
  FileText: () => <span data-testid="icon-file-text" />,
  Database: () => <span data-testid="icon-database" />,
  FileCheck: () => <span data-testid="icon-file-check" />,
}));

describe('ImportToolsPage', () => {
  it('should render with correct container spacing and title size', () => {
    const wrapper = createQueryClientWrapper();
    render(<ImportToolsPage />, { wrapper });
    
    // Get the main container
    const container = document.querySelector('.container');
    
    // Check that the container has the correct spacing classes
    expect(container).toHaveClass('container');
    expect(container).toHaveClass('mx-auto');
    expect(container).toHaveClass('px-4');
    expect(container).toHaveClass('py-8');
    
    // Check that the title has the correct size class
    const title = screen.getByRole('heading', { level: 1 });
    expect(title).toHaveClass('text-2xl');
    expect(title).toHaveClass('font-bold');
    expect(title).toHaveClass('mb-6');
    expect(title).toHaveTextContent('Import Tools');
  });
  
  it('should render tabs for different import methods', () => {
    const wrapper = createQueryClientWrapper();
    render(<ImportToolsPage />, { wrapper });
    
    // Check that the tabs are rendered
    const tabsList = document.querySelector('[data-testid="tabs-list"]');
    expect(tabsList).toBeInTheDocument();
    
    // Check that the tab triggers are rendered
    const tabTriggers = document.querySelectorAll('[data-testid="tabs-trigger"]');
    expect(tabTriggers.length).toBeGreaterThan(0);
    
    // Check that the tab content is rendered
    const tabsContent = document.querySelectorAll('[data-testid="tabs-content"]');
    expect(tabsContent.length).toBeGreaterThan(0);
  });
  
  // Additional tests for responsive behavior would typically involve
  // checking how the layout changes at different viewport sizes,
  // but this is difficult to test in a unit test environment.
  // For comprehensive responsive testing, we would need to use
  // a tool like Playwright or Cypress that can resize the viewport.
});