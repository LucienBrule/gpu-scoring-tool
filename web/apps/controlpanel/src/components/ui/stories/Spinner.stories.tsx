import type { Meta, StoryObj } from '@storybook/react-vite';
import { Spinner } from '../Spinner';

const meta: Meta<typeof Spinner> = {
  title: 'UI/Spinner',
  component: Spinner,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'The size of the spinner',
      table: {
        defaultValue: { summary: 'md' },
      },
    },
    color: {
      control: 'select',
      options: ['primary', 'secondary', 'accent', 'white'],
      description: 'The color of the spinner',
      table: {
        defaultValue: { summary: 'primary' },
      },
    },
    showText: {
      control: 'boolean',
      description: 'Whether to show a loading text below the spinner',
      table: {
        defaultValue: { summary: false },
      },
    },
    text: {
      control: 'text',
      description: 'The text to display below the spinner',
      table: {
        defaultValue: { summary: 'Loading...' },
      },
    },
  },
};

export default meta;
type Story = StoryObj<typeof Spinner>;

// Default spinner
export const Default: Story = {
  args: {
    size: 'md',
    color: 'primary',
    showText: false,
  },
};

// Small spinner
export const Small: Story = {
  args: {
    size: 'sm',
    color: 'primary',
    showText: false,
  },
};

// Large spinner
export const Large: Story = {
  args: {
    size: 'lg',
    color: 'primary',
    showText: false,
  },
};

// Spinner with text
export const WithText: Story = {
  args: {
    size: 'md',
    color: 'primary',
    showText: true,
    text: 'Loading...',
  },
};

// Spinner with custom text
export const WithCustomText: Story = {
  args: {
    size: 'md',
    color: 'primary',
    showText: true,
    text: 'Fetching data...',
  },
};

// Secondary color spinner
export const Secondary: Story = {
  args: {
    size: 'md',
    color: 'secondary',
    showText: false,
  },
};

// Accent color spinner
export const Accent: Story = {
  args: {
    size: 'md',
    color: 'accent',
    showText: false,
  },
};

// White color spinner (for dark backgrounds)
export const White: Story = {
  args: {
    size: 'md',
    color: 'white',
    showText: false,
  },
  parameters: {
    backgrounds: { default: 'dark' },
  },
};

// All sizes and colors
export const AllVariants: Story = {
  render: () => (
    <div className="grid grid-cols-4 gap-8">
      <div className="space-y-4">
        <h3 className="text-center font-medium">Small</h3>
        <Spinner size="sm" color="primary" />
        <Spinner size="sm" color="secondary" />
        <Spinner size="sm" color="accent" />
        <div className="bg-gray-800 p-4 rounded">
          <Spinner size="sm" color="white" />
        </div>
      </div>
      <div className="space-y-4">
        <h3 className="text-center font-medium">Medium</h3>
        <Spinner size="md" color="primary" />
        <Spinner size="md" color="secondary" />
        <Spinner size="md" color="accent" />
        <div className="bg-gray-800 p-4 rounded">
          <Spinner size="md" color="white" />
        </div>
      </div>
      <div className="space-y-4">
        <h3 className="text-center font-medium">Large</h3>
        <Spinner size="lg" color="primary" />
        <Spinner size="lg" color="secondary" />
        <Spinner size="lg" color="accent" />
        <div className="bg-gray-800 p-4 rounded">
          <Spinner size="lg" color="white" />
        </div>
      </div>
      <div className="space-y-4">
        <h3 className="text-center font-medium">With Text</h3>
        <Spinner size="sm" color="primary" showText text="Loading..." />
        <Spinner size="md" color="secondary" showText text="Processing..." />
        <Spinner size="lg" color="accent" showText text="Please wait..." />
        <div className="bg-gray-800 p-4 rounded">
          <Spinner size="md" color="white" showText text="Fetching..." />
        </div>
      </div>
    </div>
  ),
};