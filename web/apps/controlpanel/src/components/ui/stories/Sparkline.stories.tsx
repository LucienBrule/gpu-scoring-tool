import type { Meta, StoryObj } from '@storybook/react-vite';
import { Sparkline } from '../Sparkline';

const meta: Meta<typeof Sparkline> = {
  title: 'UI/Sparkline',
  component: Sparkline,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    data: {
      control: 'object',
      description: 'Array of numeric values to plot',
    },
    width: {
      control: { type: 'number', min: 50, max: 500, step: 10 },
      description: 'Width of the sparkline in pixels',
      table: {
        defaultValue: { summary: 100 },
      },
    },
    height: {
      control: { type: 'number', min: 10, max: 200, step: 5 },
      description: 'Height of the sparkline in pixels',
      table: {
        defaultValue: { summary: 24 },
      },
    },
    color: {
      control: 'color',
      description: 'Color of the sparkline',
      table: {
        defaultValue: { summary: 'currentColor' },
      },
    },
    strokeWidth: {
      control: { type: 'number', min: 1, max: 10, step: 1 },
      description: 'Width of the stroke in pixels',
      table: {
        defaultValue: { summary: 2 },
      },
    },
    gradientFill: {
      control: 'boolean',
      description: 'Whether to fill the area under the curve',
      table: {
        defaultValue: { summary: false },
      },
    },
  },
};

export default meta;
type Story = StoryObj<typeof Sparkline>;

// Sample data sets
const upwardTrend = [10, 15, 13, 17, 20, 22, 25, 27, 30, 35];
const downwardTrend = [35, 30, 32, 28, 25, 23, 20, 18, 15, 10];
const volatileTrend = [20, 25, 15, 30, 10, 35, 5, 25, 15, 20];
const flatTrend = [20, 20, 21, 19, 20, 21, 20, 19, 20, 20];

// Default sparkline with upward trend
export const Default: Story = {
  args: {
    data: upwardTrend,
    width: 150,
    height: 40,
    color: '#3b82f6', // blue-500
    strokeWidth: 2,
    gradientFill: false,
  },
};

// Sparkline with gradient fill
export const WithGradientFill: Story = {
  args: {
    data: upwardTrend,
    width: 150,
    height: 40,
    color: '#3b82f6', // blue-500
    strokeWidth: 2,
    gradientFill: true,
  },
};

// Downward trend
export const DownwardTrend: Story = {
  args: {
    data: downwardTrend,
    width: 150,
    height: 40,
    color: '#ef4444', // red-500
    strokeWidth: 2,
    gradientFill: false,
  },
};

// Volatile trend
export const VolatileTrend: Story = {
  args: {
    data: volatileTrend,
    width: 150,
    height: 40,
    color: '#eab308', // yellow-500
    strokeWidth: 2,
    gradientFill: false,
  },
};

// Flat trend
export const FlatTrend: Story = {
  args: {
    data: flatTrend,
    width: 150,
    height: 40,
    color: '#22c55e', // green-500
    strokeWidth: 2,
    gradientFill: false,
  },
};

// Empty data
export const EmptyData: Story = {
  args: {
    data: [],
    width: 150,
    height: 40,
    color: '#3b82f6', // blue-500
    strokeWidth: 2,
    gradientFill: false,
  },
};

// Single value data
export const SingleValue: Story = {
  args: {
    data: [25],
    width: 150,
    height: 40,
    color: '#3b82f6', // blue-500
    strokeWidth: 2,
    gradientFill: false,
  },
};

// Thicker stroke
export const ThickStroke: Story = {
  args: {
    data: upwardTrend,
    width: 150,
    height: 40,
    color: '#3b82f6', // blue-500
    strokeWidth: 4,
    gradientFill: false,
  },
};

// Compact size
export const CompactSize: Story = {
  args: {
    data: upwardTrend,
    width: 80,
    height: 20,
    color: '#3b82f6', // blue-500
    strokeWidth: 1.5,
    gradientFill: false,
  },
};

// All variants
export const AllVariants: Story = {
  render: () => (
    <div className="space-y-8 w-96 p-4">
      <div className="space-y-4">
        <h3 className="text-center font-medium">Trend Directions</h3>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Upward:</span>
          <Sparkline data={upwardTrend} width={100} height={30} color="#3b82f6" />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Downward:</span>
          <Sparkline data={downwardTrend} width={100} height={30} color="#ef4444" />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Volatile:</span>
          <Sparkline data={volatileTrend} width={100} height={30} color="#eab308" />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Flat:</span>
          <Sparkline data={flatTrend} width={100} height={30} color="#22c55e" />
        </div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-center font-medium">Fill Styles</h3>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">No Fill:</span>
          <Sparkline data={upwardTrend} width={100} height={30} color="#3b82f6" />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">With Fill:</span>
          <Sparkline data={upwardTrend} width={100} height={30} color="#3b82f6" gradientFill />
        </div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-center font-medium">Stroke Widths</h3>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Thin (1px):</span>
          <Sparkline data={upwardTrend} width={100} height={30} color="#3b82f6" strokeWidth={1} />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Medium (2px):</span>
          <Sparkline data={upwardTrend} width={100} height={30} color="#3b82f6" strokeWidth={2} />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Thick (3px):</span>
          <Sparkline data={upwardTrend} width={100} height={30} color="#3b82f6" strokeWidth={3} />
        </div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-center font-medium">Edge Cases</h3>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Empty Data:</span>
          <Sparkline data={[]} width={100} height={30} color="#3b82f6" />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Single Value:</span>
          <Sparkline data={[25]} width={100} height={30} color="#3b82f6" />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Same Values:</span>
          <Sparkline data={[20, 20, 20, 20, 20]} width={100} height={30} color="#3b82f6" />
        </div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-center font-medium">Sizes</h3>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Small:</span>
          <Sparkline data={upwardTrend} width={60} height={20} color="#3b82f6" strokeWidth={1} />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Medium:</span>
          <Sparkline data={upwardTrend} width={100} height={30} color="#3b82f6" strokeWidth={2} />
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Large:</span>
          <Sparkline data={upwardTrend} width={150} height={40} color="#3b82f6" strokeWidth={2} />
        </div>
      </div>
    </div>
  ),
};