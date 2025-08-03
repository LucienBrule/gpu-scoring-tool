import type { Meta, StoryObj } from '@storybook/react-vite';
import { ErrorBanner } from '../error-banner';
import { Button } from '../button';

const meta: Meta<typeof ErrorBanner> = {
  title: 'UI/ErrorBanner',
  component: ErrorBanner,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    title: {
      control: 'text',
      description: 'The title of the banner',
    },
    message: {
      control: 'text',
      description: 'The message to display',
    },
    severity: {
      control: 'select',
      options: ['error', 'warning', 'info', 'success'],
      description: 'The severity level of the error',
      table: {
        defaultValue: { summary: 'error' },
      },
    },
    dismissible: {
      control: 'boolean',
      description: 'Whether the banner can be dismissed',
      table: {
        defaultValue: { summary: false },
      },
    },
    onRetry: {
      action: 'retry',
      description: 'Callback function to retry the operation',
    },
    onDismiss: {
      action: 'dismiss',
      description: 'Callback function called when the banner is dismissed',
    },
  },
};

export default meta;
type Story = StoryObj<typeof ErrorBanner>;

// Error banner
export const Error: Story = {
  args: {
    title: 'Error',
    message: 'There was an error processing your request. Please try again later.',
    severity: 'error',
    dismissible: false,
  },
};

// Warning banner
export const Warning: Story = {
  args: {
    title: 'Warning',
    message: 'This action may have unintended consequences. Proceed with caution.',
    severity: 'warning',
    dismissible: false,
  },
};

// Info banner
export const Info: Story = {
  args: {
    title: 'Information',
    message: 'The system will be undergoing maintenance in 24 hours.',
    severity: 'info',
    dismissible: false,
  },
};

// Success banner
export const Success: Story = {
  args: {
    title: 'Success',
    message: 'Your changes have been saved successfully.',
    severity: 'success',
    dismissible: false,
  },
};

// Dismissible banner
export const Dismissible: Story = {
  args: {
    title: 'Dismissible Banner',
    message: 'You can dismiss this banner by clicking the X button.',
    severity: 'info',
    dismissible: true,
  },
};

// Banner with retry button
export const WithRetry: Story = {
  args: {
    title: 'Connection Error',
    message: 'Failed to connect to the server. Please check your internet connection.',
    severity: 'error',
    dismissible: false,
    onRetry: () => console.log('Retry clicked'),
  },
};

// Banner with custom content
export const WithCustomContent: Story = {
  args: {
    title: 'Custom Content',
    message: 'This banner contains custom content below the message.',
    severity: 'info',
    dismissible: false,
    children: (
      <div className="mt-2 p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
        <p className="text-sm">Here is some additional information that might be helpful.</p>
        <div className="mt-2 flex space-x-2">
          <Button size="sm" variant="outline">Learn More</Button>
          <Button size="sm">Dismiss</Button>
        </div>
      </div>
    ),
  },
};

// Empty state banner (used for no data scenarios)
export const EmptyState: Story = {
  args: {
    title: 'No Results Found',
    message: 'There are no items matching your search criteria. Try adjusting your filters.',
    severity: 'warning',
    dismissible: false,
  },
};

// All variants
export const AllVariants: Story = {
  render: () => (
    <div className="space-y-4 w-full max-w-2xl">
      <ErrorBanner
        title="Error Banner"
        message="There was an error processing your request. Please try again later."
        severity="error"
      />
      
      <ErrorBanner
        title="Warning Banner"
        message="This action may have unintended consequences. Proceed with caution."
        severity="warning"
      />
      
      <ErrorBanner
        title="Info Banner"
        message="The system will be undergoing maintenance in 24 hours."
        severity="info"
      />
      
      <ErrorBanner
        title="Success Banner"
        message="Your changes have been saved successfully."
        severity="success"
      />
      
      <ErrorBanner
        title="Dismissible Banner"
        message="You can dismiss this banner by clicking the X button."
        severity="info"
        dismissible
      />
      
      <ErrorBanner
        title="Banner with Retry"
        message="Failed to connect to the server. Please check your internet connection."
        severity="error"
        onRetry={() => console.log('Retry clicked')}
      />
      
      <ErrorBanner
        title="Empty State Example"
        message="No listings found matching your criteria. Try adjusting your filters or creating a new listing."
        severity="warning"
      >
        <div className="mt-2 flex justify-center">
          <Button size="sm" variant="outline">Clear Filters</Button>
        </div>
      </ErrorBanner>
    </div>
  ),
};