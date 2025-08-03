import type { Meta, StoryObj } from '@storybook/react-vite';
import { Skeleton } from '../skeleton';

const meta: Meta<typeof Skeleton> = {
  title: 'UI/Skeleton',
  component: Skeleton,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['text', 'circle', 'rect', 'card', 'table'],
      description: 'The variant of the skeleton',
      table: {
        defaultValue: { summary: 'text' },
      },
    },
    width: {
      control: 'text',
      description: 'The width of the skeleton (number for px, string for other units)',
    },
    height: {
      control: 'text',
      description: 'The height of the skeleton (number for px, string for other units)',
    },
    count: {
      control: { type: 'number', min: 1, max: 10 },
      description: 'The number of items to render (for text and table variants)',
      table: {
        defaultValue: { summary: 1 },
      },
    },
    animate: {
      control: 'boolean',
      description: 'Whether to show the animation',
      table: {
        defaultValue: { summary: true },
      },
    },
    borderRadius: {
      control: 'text',
      description: 'The border radius of the skeleton',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Skeleton>;

// Default text skeleton
export const Default: Story = {
  args: {
    variant: 'text',
    count: 3,
    animate: true,
  },
};

// Circle skeleton
export const Circle: Story = {
  args: {
    variant: 'circle',
    width: 80,
    height: 80,
    animate: true,
  },
};

// Rectangle skeleton
export const Rectangle: Story = {
  args: {
    variant: 'rect',
    width: 300,
    height: 150,
    animate: true,
  },
};

// Card skeleton
export const Card: Story = {
  args: {
    variant: 'card',
    width: 350,
    height: 200,
    animate: true,
  },
};

// Table skeleton
export const Table: Story = {
  args: {
    variant: 'table',
    count: 5,
    animate: true,
  },
};

// Multiple text lines with different widths
export const TextLines: Story = {
  args: {
    variant: 'text',
    count: 5,
    animate: true,
  },
};

// Non-animated skeleton
export const NoAnimation: Story = {
  args: {
    variant: 'text',
    count: 3,
    animate: false,
  },
};

// Custom border radius
export const CustomBorderRadius: Story = {
  args: {
    variant: 'rect',
    width: 300,
    height: 150,
    borderRadius: '1.5rem',
    animate: true,
  },
};

// All variants
export const AllVariants: Story = {
  render: () => (
    <div className="space-y-8 w-full max-w-2xl">
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Text Skeleton</h3>
        <Skeleton variant="text" count={3} />
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Circle Skeleton</h3>
        <div className="flex space-x-4">
          <Skeleton variant="circle" width={40} height={40} />
          <Skeleton variant="circle" width={60} height={60} />
          <Skeleton variant="circle" width={80} height={80} />
        </div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Rectangle Skeleton</h3>
        <Skeleton variant="rect" width="100%" height={100} />
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Card Skeleton</h3>
        <Skeleton variant="card" width="100%" height={200} />
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Table Skeleton</h3>
        <Skeleton variant="table" count={3} />
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Profile Card Example</h3>
        <div className="flex space-x-4 items-center p-4 border border-gray-200 rounded-lg">
          <Skeleton variant="circle" width={60} height={60} />
          <div className="flex-1">
            <Skeleton variant="text" width="60%" height={20} count={1} />
            <Skeleton variant="text" width="40%" height={16} count={1} className="mt-2" />
          </div>
        </div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Content Layout Example</h3>
        <div className="space-y-4 p-4 border border-gray-200 rounded-lg">
          <Skeleton variant="text" width="80%" height={24} count={1} />
          <Skeleton variant="text" count={2} />
          <Skeleton variant="rect" width="100%" height={200} />
          <Skeleton variant="text" count={3} />
        </div>
      </div>
    </div>
  ),
};