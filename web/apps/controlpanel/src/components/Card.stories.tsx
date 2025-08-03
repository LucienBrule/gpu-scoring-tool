import type { Meta, StoryObj } from '@storybook/react-vite';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@repo/ui/card';
import { Button } from '@repo/ui/button';

const meta: Meta<typeof Card> = {
  title: 'UI/Card',
  component: Card,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    className: {
      control: 'text',
      description: 'Additional CSS classes to apply',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Card>;

// Basic card
export const Basic: Story = {
  args: {
    className: 'w-[350px]',
    children: (
      <>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Card Content</p>
        </CardContent>
      </>
    ),
  },
};

// Card with footer
export const WithFooter: Story = {
  args: {
    className: 'w-[350px]',
    children: (
      <>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Card Content</p>
        </CardContent>
        <CardFooter>
          <Button size="sm">Action</Button>
        </CardFooter>
      </>
    ),
  },
};

// Card with multiple actions
export const WithActions: Story = {
  args: {
    className: 'w-[350px]',
    children: (
      <>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card with multiple actions</CardDescription>
        </CardHeader>
        <CardContent>
          <p>This card has multiple actions in the footer.</p>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline" size="sm">Cancel</Button>
          <Button size="sm">Save</Button>
        </CardFooter>
      </>
    ),
  },
};

// Card with image
export const WithImage: Story = {
  args: {
    className: 'w-[350px] overflow-hidden',
    children: (
      <>
        <div className="h-[200px] bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
          <span className="text-gray-500 dark:text-gray-400">Image Placeholder</span>
        </div>
        <CardHeader>
          <CardTitle>Card with Image</CardTitle>
          <CardDescription>This card has an image at the top</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Card content goes here.</p>
        </CardContent>
      </>
    ),
  },
};

// Card with custom styling
export const CustomStyling: Story = {
  args: {
    className: 'w-[350px] border-blue-500 dark:border-blue-400',
    children: (
      <>
        <CardHeader className="bg-blue-50 dark:bg-blue-900/20">
          <CardTitle className="text-blue-700 dark:text-blue-300">Custom Styled Card</CardTitle>
          <CardDescription>This card has custom styling</CardDescription>
        </CardHeader>
        <CardContent>
          <p>You can customize the appearance of cards with additional classes.</p>
        </CardContent>
        <CardFooter className="bg-gray-50 dark:bg-gray-800">
          <Button variant="outline" size="sm">Learn More</Button>
        </CardFooter>
      </>
    ),
  },
};

// Multiple cards layout
export const MultipleCards: Story = {
  render: () => (
    <div className="grid grid-cols-2 gap-4 max-w-[750px]">
      <Card>
        <CardHeader>
          <CardTitle>First Card</CardTitle>
          <CardDescription>Description for first card</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Content for the first card.</p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Second Card</CardTitle>
          <CardDescription>Description for second card</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Content for the second card.</p>
        </CardContent>
      </Card>
      
      <Card className="col-span-2">
        <CardHeader>
          <CardTitle>Full Width Card</CardTitle>
          <CardDescription>This card spans the full width</CardDescription>
        </CardHeader>
        <CardContent>
          <p>This card takes up the full width of the container.</p>
        </CardContent>
        <CardFooter>
          <Button size="sm">Action</Button>
        </CardFooter>
      </Card>
    </div>
  ),
};