import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ErrorBanner } from '../error-banner';

describe('ErrorBanner', () => {
  // Test default rendering
  it('renders error severity by default', () => {
    render(<ErrorBanner message="An error occurred" />);
    const banner = screen.getByTestId('error-banner-error');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveTextContent('An error occurred');
  });

  // Test different severity levels
  it('renders warning severity correctly', () => {
    render(<ErrorBanner message="Warning message" severity="warning" />);
    const banner = screen.getByTestId('error-banner-warning');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveTextContent('Warning message');
  });

  it('renders info severity correctly', () => {
    render(<ErrorBanner message="Info message" severity="info" />);
    const banner = screen.getByTestId('error-banner-info');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveTextContent('Info message');
  });

  it('renders success severity correctly', () => {
    render(<ErrorBanner message="Success message" severity="success" />);
    const banner = screen.getByTestId('error-banner-success');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveTextContent('Success message');
  });

  // Test title rendering
  it('renders title when provided', () => {
    render(<ErrorBanner title="Error Title" message="Error message" />);
    expect(screen.getByText('Error Title')).toBeInTheDocument();
    expect(screen.getByText('Error message')).toBeInTheDocument();
  });

  // Test retry functionality
  it('renders retry button when onRetry is provided', () => {
    const handleRetry = vi.fn();
    render(<ErrorBanner message="Error message" onRetry={handleRetry} />);
    
    const retryButton = screen.getByTestId('error-banner-retry');
    expect(retryButton).toBeInTheDocument();
    
    // Click the retry button
    fireEvent.click(retryButton);
    expect(handleRetry).toHaveBeenCalledTimes(1);
  });

  it('does not render retry button when onRetry is not provided', () => {
    render(<ErrorBanner message="Error message" />);
    expect(screen.queryByTestId('error-banner-retry')).not.toBeInTheDocument();
  });

  // Test dismissible functionality
  it('renders dismiss button when dismissible is true', () => {
    render(<ErrorBanner message="Error message" dismissible />);
    
    const dismissButton = screen.getByTestId('error-banner-dismiss');
    expect(dismissButton).toBeInTheDocument();
  });

  it('does not render dismiss button when dismissible is false', () => {
    render(<ErrorBanner message="Error message" dismissible={false} />);
    expect(screen.queryByTestId('error-banner-dismiss')).not.toBeInTheDocument();
  });

  it('calls onDismiss when dismiss button is clicked', () => {
    const handleDismiss = vi.fn();
    render(<ErrorBanner message="Error message" dismissible onDismiss={handleDismiss} />);
    
    const dismissButton = screen.getByTestId('error-banner-dismiss');
    fireEvent.click(dismissButton);
    
    expect(handleDismiss).toHaveBeenCalledTimes(1);
  });

  it('hides the banner when dismiss button is clicked', () => {
    render(<ErrorBanner message="Error message" dismissible />);
    
    const dismissButton = screen.getByTestId('error-banner-dismiss');
    fireEvent.click(dismissButton);
    
    // Banner should no longer be in the document
    expect(screen.queryByTestId('error-banner-error')).not.toBeInTheDocument();
  });

  // Test accessibility
  it('has correct accessibility attributes for error severity', () => {
    render(<ErrorBanner message="Error message" severity="error" />);
    const banner = screen.getByTestId('error-banner-error');
    
    expect(banner).toHaveAttribute('role', 'alert');
    expect(banner).toHaveAttribute('aria-live', 'assertive');
  });

  it('has correct accessibility attributes for non-error severity', () => {
    render(<ErrorBanner message="Info message" severity="info" />);
    const banner = screen.getByTestId('error-banner-info');
    
    expect(banner).toHaveAttribute('role', 'status');
    expect(banner).toHaveAttribute('aria-live', 'polite');
  });

  // Test custom className
  it('applies custom class name', () => {
    render(<ErrorBanner message="Error message" className="custom-class" />);
    const banner = screen.getByTestId('error-banner-error');
    
    expect(banner).toHaveClass('custom-class');
  });

  // Test children rendering
  it('renders children when provided', () => {
    render(
      <ErrorBanner message="Error message">
        <div data-testid="child-element">Additional content</div>
      </ErrorBanner>
    );
    
    const childElement = screen.getByTestId('child-element');
    expect(childElement).toBeInTheDocument();
    expect(childElement).toHaveTextContent('Additional content');
  });
});