import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Skeleton } from '../skeleton';

describe('Skeleton', () => {
  // Test default rendering
  it('renders text variant by default', () => {
    render(<Skeleton />);
    const skeleton = screen.getByTestId('skeleton-text');
    expect(skeleton).toBeInTheDocument();
  });

  // Test different variants
  it('renders circle variant correctly', () => {
    render(<Skeleton variant="circle" />);
    const skeleton = screen.getByTestId('skeleton-circle');
    expect(skeleton).toBeInTheDocument();
    expect(skeleton).toHaveStyle('border-radius: 50%');
  });

  it('renders rect variant correctly', () => {
    render(<Skeleton variant="rect" />);
    const skeleton = screen.getByTestId('skeleton-rect');
    expect(skeleton).toBeInTheDocument();
  });

  it('renders card variant correctly', () => {
    render(<Skeleton variant="card" />);
    const skeleton = screen.getByTestId('skeleton-card');
    expect(skeleton).toBeInTheDocument();
    
    // Card should have inner elements for the card content
    const innerElements = skeleton.querySelectorAll('div > div');
    expect(innerElements.length).toBeGreaterThan(0);
  });

  it('renders table variant correctly', () => {
    render(<Skeleton variant="table" count={3} />);
    const skeleton = screen.getByTestId('skeleton-table');
    expect(skeleton).toBeInTheDocument();
    
    // Should have 3 rows
    const rows = skeleton.querySelectorAll('div > div');
    expect(rows.length).toBe(3);
  });

  // Test customization props
  it('applies custom width and height', () => {
    render(<Skeleton variant="rect" width={200} height={100} />);
    const skeleton = screen.getByTestId('skeleton-rect');
    expect(skeleton).toHaveStyle('width: 200px');
    expect(skeleton).toHaveStyle('height: 100px');
  });

  it('applies string width and height values', () => {
    render(<Skeleton variant="rect" width="50%" height="10rem" />);
    const skeleton = screen.getByTestId('skeleton-rect');
    expect(skeleton).toHaveStyle('width: 50%');
    expect(skeleton).toHaveStyle('height: 10rem');
  });

  it('applies custom border radius', () => {
    render(<Skeleton variant="rect" borderRadius="1rem" />);
    const skeleton = screen.getByTestId('skeleton-rect');
    expect(skeleton).toHaveStyle('border-radius: 1rem');
  });

  it('applies custom class name', () => {
    render(<Skeleton variant="rect" className="custom-class" />);
    const skeleton = screen.getByTestId('skeleton-rect');
    expect(skeleton).toHaveClass('custom-class');
  });

  it('disables animation when animate is false', () => {
    render(<Skeleton variant="rect" animate={false} />);
    const skeleton = screen.getByTestId('skeleton-rect');
    expect(skeleton.className).not.toContain('animate-pulse');
  });

  // Test count prop for text variant
  it('renders correct number of text lines', () => {
    render(<Skeleton variant="text" count={3} />);
    const skeleton = screen.getByTestId('skeleton-text');
    const lines = skeleton.querySelectorAll('div > div');
    expect(lines.length).toBe(3);
  });

  // Test accessibility
  it('has aria-hidden attribute', () => {
    render(<Skeleton variant="rect" />);
    const skeleton = screen.getByTestId('skeleton-rect');
    expect(skeleton).toHaveAttribute('aria-hidden', 'true');
  });

  // Test children rendering
  it('renders children when provided', () => {
    render(
      <Skeleton variant="rect">
        <div data-testid="child-element">Custom content</div>
      </Skeleton>
    );
    const childElement = screen.getByTestId('child-element');
    expect(childElement).toBeInTheDocument();
    expect(childElement).toHaveTextContent('Custom content');
  });
});