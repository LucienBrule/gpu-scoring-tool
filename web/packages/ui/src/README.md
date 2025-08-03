# UI Component Library

This directory contains standardized UI components for the GPU Scoring Tool Control Panel. These components follow a consistent pattern and are designed to work well together, providing a cohesive user experience.

## Component Structure

All components follow a similar structure:

1. **Client-side rendering**: All components use the `"use client"` directive to ensure they work with Next.js App Router.
2. **ForwardRef**: Components that render HTML elements use `forwardRef` to allow ref forwarding.
3. **TypeScript interfaces**: All components have TypeScript interfaces for their props.
4. **Styling**: Components use Tailwind CSS for styling, with support for dark mode.
5. **Display names**: Components have display names for better debugging.

## Available Components

### Alert

The Alert component is used to display important messages to the user.

```tsx
<Alert variant="destructive">
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Something went wrong.</AlertDescription>
</Alert>
```

**Variants**: default, destructive, success, warning, info

### Button

The Button component is used for actions and navigation.

```tsx
<Button variant="default" size="default">
  Click me
</Button>
```

**Variants**: default, destructive, outline, secondary, ghost, link  
**Sizes**: default, sm, lg, icon

### Checkbox

The Checkbox component is used for boolean input.

```tsx
<Checkbox
  checked={checked}
  onCheckedChange={setChecked}
  id="terms"
/>
<Label htmlFor="terms">Accept terms and conditions</Label>
```

### Input

The Input component is used for text input.

```tsx
<Input
  type="text"
  placeholder="Enter your name"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

### Label

The Label component is used to label form elements.

```tsx
<Label htmlFor="email">Email</Label>
<Input id="email" type="email" />
```

### Select

The Select component is used for selecting from a list of options.

```tsx
<Select value={value} onValueChange={setValue}>
  <SelectTrigger>
    <SelectValue placeholder="Select an option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">Option 1</SelectItem>
    <SelectItem value="option2">Option 2</SelectItem>
  </SelectContent>
</Select>
```

### Tabs

The Tabs component is used for tabbed interfaces.

```tsx
<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
    <TabsTrigger value="tab2">Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">Content for Tab 1</TabsContent>
  <TabsContent value="tab2">Content for Tab 2</TabsContent>
</Tabs>
```

## Utility Functions

### cn

The `cn` utility function is used to merge class names with conditional logic.

```tsx
import { cn } from "./utils";

<div className={cn("base-class", condition && "conditional-class", className)}>
  Content
</div>
```

## Dark Mode Support

All components support dark mode with appropriate Tailwind CSS classes. Dark mode is enabled by adding the `dark` class to the `<html>` element, which is done by default in the application.

## Accessibility

All components are designed with accessibility in mind, including:

- Proper ARIA attributes
- Keyboard navigation
- Focus management
- Color contrast

## Extending Components

When creating new components, follow these guidelines:

1. Use the existing components as a starting point
2. Follow the same structure and patterns
3. Ensure dark mode support
4. Add proper TypeScript types
5. Include JSDoc comments for documentation
6. Add display names for debugging
7. Test with different screen sizes and color schemes