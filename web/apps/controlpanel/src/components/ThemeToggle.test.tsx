import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import ThemeToggle from './ThemeToggle';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value.toString();
    }),
    clear: vi.fn(() => {
      store = {};
    }),
  };
})();

// Mock document methods
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock document.documentElement
const mockAdd = vi.fn();
const mockRemove = vi.fn();
document.documentElement.classList = {
  add: mockAdd,
  remove: mockRemove,
  // Add other required DOMTokenList methods as needed
  contains: vi.fn(),
  toggle: vi.fn(),
  replace: vi.fn(),
  supports: vi.fn(),
  value: '',
  length: 0,
  item: vi.fn(),
  forEach: vi.fn(),
  entries: vi.fn(),
  keys: vi.fn(),
  values: vi.fn(),
  [Symbol.iterator]: vi.fn(),
} as DOMTokenList;

describe('ThemeToggle Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorageMock.clear();
  });

  it('renders correctly in light mode', async () => {
    // Mock localStorage to return 'light'
    localStorageMock.getItem.mockReturnValueOnce('light');
    
    let container;
    await act(async () => {
      const result = render(<ThemeToggle />);
      container = result.container;
    });
    
    expect(container).toMatchSnapshot();
    
    // Check if the button text is correct for light mode
    expect(screen.getByText(/Dark Mode/i)).toBeInTheDocument();
  });

  it('renders correctly in dark mode', async () => {
    // Mock localStorage to return 'dark'
    localStorageMock.getItem.mockReturnValueOnce('dark');
    
    let container;
    await act(async () => {
      const result = render(<ThemeToggle />);
      container = result.container;
    });
    
    expect(container).toMatchSnapshot();
    
    // Check if the button text is correct for dark mode
    expect(screen.getByText(/Light Mode/i)).toBeInTheDocument();
  });

  it('defaults to dark mode when no preference is stored', async () => {
    // Mock localStorage to return null (no stored preference)
    localStorageMock.getItem.mockReturnValueOnce(null);
    
    // Mock matchMedia to return false for dark mode preference
    Object.defineProperty(window, 'matchMedia', {
      value: vi.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })),
    });
    
    await act(async () => {
      render(<ThemeToggle />);
    });
    
    // Check if the button text is correct for light mode (default)
    expect(screen.getByText(/Dark Mode/i)).toBeInTheDocument();
  });

  it('uses system preference when no preference is stored', async () => {
    // Mock localStorage to return null (no stored preference)
    localStorageMock.getItem.mockReturnValueOnce(null);
    
    // Mock matchMedia to return true for dark mode preference
    Object.defineProperty(window, 'matchMedia', {
      value: vi.fn().mockImplementation((query) => ({
        matches: query === '(prefers-color-scheme: dark)',
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })),
    });
    
    await act(async () => {
      render(<ThemeToggle />);
    });
    
    // Check if the button text is correct for dark mode (system preference)
    expect(screen.getByText(/Light Mode/i)).toBeInTheDocument();
  });
});