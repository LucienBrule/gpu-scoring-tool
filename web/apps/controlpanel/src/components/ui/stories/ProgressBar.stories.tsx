import type { Meta, StoryObj } from '@storybook/react-vite';
import { ProgressBar } from '../ProgressBar';

const meta: Meta<typeof ProgressBar> = {
  title: 'UI/ProgressBar',
  component: ProgressBar,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    value: {
      control: { type: 'range', min: 0, max: 100, step: 1 },
      description: 'The current progress value (0-100)',
    },
    color: {
      control: 'select',
      options: ['primary', 'secondary', 'accent', 'success', 'warning', 'danger'],
      description: 'The color of the progress bar',
      table: {
        defaultValue: { summary: 'primary' },
      },
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'The size/height of the progress bar',
      table: {
        defaultValue: { summary: 'md' },
      },
    },
    showText: {
      control: 'boolean',
      description: 'Whether to show the progress text',
      table: {
        defaultValue: { summary: false },
      },
    },
    text: {
      control: 'text',
      description: 'Custom text to display. If not provided, shows "{value}%"',
    },
  },
};

export default meta;
type Story = StoryObj<typeof ProgressBar>;

// Default progress bar
export const Default: Story = {
  args: {
    value: 50,
    color: 'primary',
    size: 'md',
    showText: false,
  },
};

// Small progress bar
export const Small: Story = {
  args: {
    value: 50,
    color: 'primary',
    size: 'sm',
    showText: false,
  },
};

// Large progress bar
export const Large: Story = {
  args: {
    value: 50,
    color: 'primary',
    size: 'lg',
    showText: false,
  },
};

// Progress bar with text
export const WithText: Story = {
  args: {
    value: 50,
    color: 'primary',
    size: 'md',
    showText: true,
  },
};

// Progress bar with custom text
export const WithCustomText: Story = {
  args: {
    value: 50,
    color: 'primary',
    size: 'md',
    showText: true,
    text: 'Uploading file... 50%',
  },
};

// Success progress bar
export const Success: Story = {
  args: {
    value: 75,
    color: 'success',
    size: 'md',
    showText: true,
  },
};

// Warning progress bar
export const Warning: Story = {
  args: {
    value: 30,
    color: 'warning',
    size: 'md',
    showText: true,
  },
};

// Danger progress bar
export const Danger: Story = {
  args: {
    value: 15,
    color: 'danger',
    size: 'md',
    showText: true,
  },
};

// Progress bar at 0%
export const Empty: Story = {
  args: {
    value: 0,
    color: 'primary',
    size: 'md',
    showText: true,
  },
};

// Progress bar at 100%
export const Complete: Story = {
  args: {
    value: 100,
    color: 'success',
    size: 'md',
    showText: true,
  },
};

// All variants
export const AllVariants: Story = {
  render: () => (
    <div className="space-y-8 w-96">
      <div className="space-y-4">
        <h3 className="text-center font-medium">Sizes</h3>
        <ProgressBar value={50} size="sm" showText />
        <ProgressBar value={50} size="md" showText />
        <ProgressBar value={50} size="lg" showText />
      </div>
      
      <div className="space-y-4">
        <h3 className="text-center font-medium">Colors</h3>
        <ProgressBar value={50} color="primary" showText />
        <ProgressBar value={50} color="secondary" showText />
        <ProgressBar value={50} color="accent" showText />
        <ProgressBar value={50} color="success" showText />
        <ProgressBar value={50} color="warning" showText />
        <ProgressBar value={50} color="danger" showText />
      </div>
      
      <div className="space-y-4">
        <h3 className="text-center font-medium">Progress States</h3>
        <ProgressBar value={0} color="primary" showText />
        <ProgressBar value={25} color="primary" showText />
        <ProgressBar value={50} color="primary" showText />
        <ProgressBar value={75} color="primary" showText />
        <ProgressBar value={100} color="success" showText />
      </div>
      
      <div className="space-y-4">
        <h3 className="text-center font-medium">Custom Text</h3>
        <ProgressBar value={25} color="primary" showText text="Connecting..." />
        <ProgressBar value={50} color="primary" showText text="Uploading file..." />
        <ProgressBar value={75} color="warning" showText text="Processing data..." />
        <ProgressBar value={100} color="success" showText text="Upload complete!" />
      </div>
    </div>
  ),
};