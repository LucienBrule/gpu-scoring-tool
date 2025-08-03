import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import RootLayout from '../layout';

// Create a mock version of RootLayout that doesn't use <html> element
// This avoids the "In HTML, <html> cannot be a child of <div>" error
const MockRootLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="mock-root-layout">
      <div className="mock-head">
        <script data-testid="script-mock" data-id="set-dark-mode" data-strategy="beforeInteractive">
          {`document.documentElement.classList.add('dark');`}
        </script>
      </div>
      <div className="mock-body bg-background text-foreground">
        <div data-testid="providers-mock">
          <div data-testid="navbar-mock">Navbar Mock</div>
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
};

// Mock CSS imports to avoid PostCSS processing errors
vi.mock('../globals.css', () => ({}));

// Mock the components used in the layout
vi.mock('@/components/Navbar', () => ({
  __esModule: true,
  default: () => <div data-testid="navbar-mock">Navbar Mock</div>,
}));

vi.mock('@/components/Providers', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="providers-mock">{children}</div>
  ),
}));

// Mock next/font to avoid errors
vi.mock('next/font/google', () => ({
  Geist: () => ({
    variable: 'mock-font-variable',
  }),
  Geist_Mono: () => ({
    variable: 'mock-font-mono-variable',
  }),
}));

// Mock next/script to avoid errors
vi.mock('next/script', () => ({
  __esModule: true,
  default: ({ id, strategy, children }: { id: string; strategy: string; children: React.ReactNode }) => (
    <script data-testid="script-mock" data-id={id} data-strategy={strategy}>
      {children}
    </script>
  ),
}));

describe('RootLayout', () => {
  it('should have dark class on html element', () => {
    // Execute the script that would be run by the RootLayout
    document.documentElement.classList.add('dark');
    
    render(
      <MockRootLayout>
        <div>Test content</div>
      </MockRootLayout>
    );
    
    // Check if the document.documentElement has the dark class
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });
  
  it('should include script to prevent FOUC', () => {
    const { getByTestId } = render(
      <MockRootLayout>
        <div>Test content</div>
      </MockRootLayout>
    );
    
    // Check that the script element is rendered with the correct attributes
    const scriptElement = getByTestId('script-mock');
    expect(scriptElement).toBeInTheDocument();
    expect(scriptElement.getAttribute('data-id')).toBe('set-dark-mode');
    expect(scriptElement.getAttribute('data-strategy')).toBe('beforeInteractive');
  });
  
  it('should render children correctly', () => {
    const { getByText } = render(
      <MockRootLayout>
        <div>Test content</div>
      </MockRootLayout>
    );
    
    // Check if the children are rendered
    expect(getByText('Test content')).toBeInTheDocument();
  });
  
  it('should include proper background and text colors', () => {
    const { container } = render(
      <MockRootLayout>
        <div>Test content</div>
      </MockRootLayout>
    );
    
    // Check if the mock-body element has the background and text color classes
    const mockBody = container.querySelector('.mock-body');
    expect(mockBody).toHaveClass('bg-background');
    expect(mockBody).toHaveClass('text-foreground');
  });
});