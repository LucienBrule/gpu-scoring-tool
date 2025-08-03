import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Sparkline } from '../Sparkline';

describe('Sparkline', () => {
  // Test default rendering
  it('renders correctly with default props', () => {
    const data = [10, 20, 30, 25, 40];
    render(<Sparkline data={data} />);
    
    // Check that the SVG element exists
    const svg = screen.getByRole('img');
    expect(svg).toBeInTheDocument();
    
    // Check that the path element exists
    const path = screen.getByTestId('sparkline-path');
    expect(path).toBeInTheDocument();
    
    // Check default attributes
    expect(svg).toHaveAttribute('width', '100');
    expect(svg).toHaveAttribute('height', '24');
    expect(path).toHaveAttribute('stroke-width', '2');
  });

  // Test custom dimensions
  it('applies custom width and height', () => {
    const data = [10, 20, 30, 25, 40];
    render(<Sparkline data={data} width={200} height={50} />);
    
    const svg = screen.getByRole('img');
    expect(svg).toHaveAttribute('width', '200');
    expect(svg).toHaveAttribute('height', '50');
    expect(svg).toHaveAttribute('viewBox', '0 0 200 50');
  });

  // Test custom styling
  it('applies custom color and stroke width', () => {
    const data = [10, 20, 30, 25, 40];
    render(<Sparkline data={data} color="#ff0000" strokeWidth={4} />);
    
    const path = screen.getByTestId('sparkline-path');
    expect(path).toHaveAttribute('stroke', '#ff0000');
    expect(path).toHaveAttribute('stroke-width', '4');
  });

  // Test gradient fill
  it('renders gradient fill when gradientFill is true', () => {
    const data = [10, 20, 30, 25, 40];
    render(<Sparkline data={data} gradientFill />);
    
    // Check that the gradient elements exist
    const defs = document.querySelector('defs');
    expect(defs).toBeInTheDocument();
    
    const linearGradient = document.querySelector('linearGradient');
    expect(linearGradient).toBeInTheDocument();
    
    const fillPath = screen.getByTestId('sparkline-fill');
    expect(fillPath).toBeInTheDocument();
    expect(fillPath).toHaveAttribute('fill', expect.stringMatching(/^url\(#sparkline-gradient-/));
  });

  // Test empty data
  it('renders a flat line when data is empty', () => {
    render(<Sparkline data={[]} />);
    
    const path = screen.getByTestId('sparkline-path');
    expect(path).toHaveAttribute('d', 'M0,12 L100,12');
  });

  // Test single value data
  it('renders a flat line when data has only one value', () => {
    render(<Sparkline data={[25]} />);
    
    const path = screen.getByTestId('sparkline-path');
    expect(path).toHaveAttribute('d', 'M0,12 L100,12');
  });

  // Test same values data
  it('renders a flat line when all data values are the same', () => {
    render(<Sparkline data={[10, 10, 10, 10]} />);
    
    const path = screen.getByTestId('sparkline-path');
    expect(path).toHaveAttribute('d', 'M0,12 L100,12');
  });

  // Test aria-label
  it('includes data summary in aria-label', () => {
    const data = [10, 20, 30, 25, 40];
    render(<Sparkline data={data} />);
    
    const svg = screen.getByRole('img');
    expect(svg).toHaveAttribute('aria-label', expect.stringMatching(/Sparkline with 5 points/));
    expect(svg).toHaveAttribute('aria-label', expect.stringMatching(/upward trend/));
  });

  // Test downward trend aria-label
  it('describes downward trend in aria-label', () => {
    const data = [40, 30, 20, 10];
    render(<Sparkline data={data} />);
    
    const svg = screen.getByRole('img');
    expect(svg).toHaveAttribute('aria-label', expect.stringMatching(/downward trend/));
  });

  // Test flat trend aria-label
  it('describes flat trend in aria-label', () => {
    const data = [20, 20, 21, 19, 20];
    render(<Sparkline data={data} />);
    
    const svg = screen.getByRole('img');
    expect(svg).toHaveAttribute('aria-label', expect.stringMatching(/flat trend/));
  });

  // Test empty data aria-label
  it('has appropriate aria-label for empty data', () => {
    render(<Sparkline data={[]} />);
    
    const svg = screen.getByRole('img');
    expect(svg).toHaveAttribute('aria-label', 'Empty sparkline');
  });
});