import type { Meta, StoryObj } from '@storybook/react-vite';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@repo/ui/tabs';
import { Card, CardContent } from '@repo/ui/card';

const meta: Meta<typeof Tabs> = {
  title: 'UI/Tabs',
  component: Tabs,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    defaultValue: {
      control: 'text',
      description: 'The default selected tab value',
    },
    value: {
      control: 'text',
      description: 'The controlled value of the selected tab',
    },
    onValueChange: {
      action: 'valueChanged',
      description: 'Callback when the selected tab changes',
    },
    className: {
      control: 'text',
      description: 'Additional CSS classes to apply',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Tabs>;

// Basic tabs
export const Basic: Story = {
  args: {
    defaultValue: 'tab1',
    className: 'w-[400px]',
    children: (
      <>
        <TabsList>
          <TabsTrigger value="tab1">Tab 1</TabsTrigger>
          <TabsTrigger value="tab2">Tab 2</TabsTrigger>
          <TabsTrigger value="tab3">Tab 3</TabsTrigger>
        </TabsList>
        <TabsContent value="tab1">
          <div className="p-4 rounded-md bg-white dark:bg-gray-800 mt-2">
            <p>Content for Tab 1</p>
          </div>
        </TabsContent>
        <TabsContent value="tab2">
          <div className="p-4 rounded-md bg-white dark:bg-gray-800 mt-2">
            <p>Content for Tab 2</p>
          </div>
        </TabsContent>
        <TabsContent value="tab3">
          <div className="p-4 rounded-md bg-white dark:bg-gray-800 mt-2">
            <p>Content for Tab 3</p>
          </div>
        </TabsContent>
      </>
    ),
  },
};

// Tabs with icons
export const WithIcons: Story = {
  args: {
    defaultValue: 'account',
    className: 'w-[400px]',
    children: (
      <>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="account">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="mr-2"
            >
              <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            Account
          </TabsTrigger>
          <TabsTrigger value="settings">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="mr-2"
            >
              <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            Settings
          </TabsTrigger>
          <TabsTrigger value="notifications">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="mr-2"
            >
              <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
              <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
            </svg>
            Notifications
          </TabsTrigger>
        </TabsList>
        <TabsContent value="account">
          <Card>
            <CardContent className="pt-4">
              <p>Account settings and preferences.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="settings">
          <Card>
            <CardContent className="pt-4">
              <p>Application settings and configuration options.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="notifications">
          <Card>
            <CardContent className="pt-4">
              <p>Manage your notification preferences.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </>
    ),
  },
};

// Tabs with different content types
export const DifferentContentTypes: Story = {
  args: {
    defaultValue: 'text',
    className: 'w-[500px]',
    children: (
      <>
        <TabsList>
          <TabsTrigger value="text">Text</TabsTrigger>
          <TabsTrigger value="form">Form</TabsTrigger>
          <TabsTrigger value="chart">Chart</TabsTrigger>
        </TabsList>
        <TabsContent value="text">
          <Card>
            <CardContent className="pt-4">
              <h3 className="text-lg font-medium mb-2">Text Content</h3>
              <p>This tab contains simple text content. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="form">
          <Card>
            <CardContent className="pt-4">
              <h3 className="text-lg font-medium mb-2">Form Content</h3>
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Name</label>
                  <input type="text" className="w-full p-2 border rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Email</label>
                  <input type="email" className="w-full p-2 border rounded-md" />
                </div>
                <button type="button" className="px-4 py-2 bg-blue-500 text-white rounded-md">Submit</button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="chart">
          <Card>
            <CardContent className="pt-4">
              <h3 className="text-lg font-medium mb-2">Chart Content</h3>
              <div className="h-[200px] bg-gray-100 dark:bg-gray-700 rounded-md flex items-center justify-center">
                <p className="text-gray-500 dark:text-gray-400">Chart Placeholder</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </>
    ),
  },
};

// Vertical tabs layout
export const VerticalLayout: Story = {
  render: () => (
    <div className="flex gap-4 w-[600px]">
      <Tabs defaultValue="tab1" className="w-full">
        <div className="flex">
          <TabsList className="flex-col h-auto mr-4">
            <TabsTrigger value="tab1" className="justify-start">Tab 1</TabsTrigger>
            <TabsTrigger value="tab2" className="justify-start">Tab 2</TabsTrigger>
            <TabsTrigger value="tab3" className="justify-start">Tab 3</TabsTrigger>
          </TabsList>
          <div className="flex-1">
            <TabsContent value="tab1">
              <Card>
                <CardContent className="pt-4">
                  <h3 className="text-lg font-medium mb-2">Tab 1 Content</h3>
                  <p>This is the content for Tab 1 in a vertical layout.</p>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="tab2">
              <Card>
                <CardContent className="pt-4">
                  <h3 className="text-lg font-medium mb-2">Tab 2 Content</h3>
                  <p>This is the content for Tab 2 in a vertical layout.</p>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="tab3">
              <Card>
                <CardContent className="pt-4">
                  <h3 className="text-lg font-medium mb-2">Tab 3 Content</h3>
                  <p>This is the content for Tab 3 in a vertical layout.</p>
                </CardContent>
              </Card>
            </TabsContent>
          </div>
        </div>
      </Tabs>
    </div>
  ),
};