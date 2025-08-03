# Loading and Empty State UI Components

This document outlines the standard patterns for displaying loading indicators and empty-state placeholders across the GPU Scoring Tool control panel application.

## Overview

Consistent loading and empty state UI feedback is essential for providing a good user experience during asynchronous operations and when no data is available. This document describes the components available for these scenarios and provides guidelines for their usage.

## Components

### Spinner

The `Spinner` component is used to indicate loading states when fetching data or performing asynchronous operations.

```tsx
import { Spinner } from "@/components/ui/Spinner";

// Basic usage
<Spinner />

// With size and color options
<Spinner size="md" color="primary" />

// With text
<Spinner size="md" color="primary" showText text="Loading..." />

// With custom text
<Spinner size="md" color="primary" showText text="Fetching data..." />
```

#### Props

- `size`: "sm" | "md" | "lg" (default: "md")
- `color`: "primary" | "secondary" | "accent" | "white" (default: "primary")
- `showText`: boolean (default: false)
- `text`: string (default: "Loading...")
- `className`: string (optional)
- `containerClassName`: string (optional)

### ProgressBar

The `ProgressBar` component is used to show progress for operations like file uploads or multi-step processes.

```tsx
import { ProgressBar } from "@/components/ui/ProgressBar";

// Basic usage
<ProgressBar value={50} />

// With color and size options
<ProgressBar value={50} color="primary" size="md" />

// With text
<ProgressBar value={50} color="primary" size="md" showText />

// With custom text
<ProgressBar value={50} color="primary" size="md" showText text="Uploading file..." />
```

#### Props

- `value`: number (0-100)
- `color`: "primary" | "secondary" | "accent" | "success" | "warning" | "danger" (default: "primary")
- `size`: "sm" | "md" | "lg" (default: "md")
- `showText`: boolean (default: false)
- `text`: string (optional, defaults to "{value}%")
- `className`: string (optional)
- `progressClassName`: string (optional)
- `textClassName`: string (optional)

### Skeleton

The `Skeleton` component is used to show a placeholder for content that is loading.

```tsx
import { Skeleton } from "@/components/ui/skeleton";

// Text skeleton
<Skeleton variant="text" count={3} />

// Circle skeleton
<Skeleton variant="circle" width={60} height={60} />

// Rectangle skeleton
<Skeleton variant="rect" width="100%" height={200} />

// Card skeleton
<Skeleton variant="card" width="100%" height={200} />

// Table skeleton
<Skeleton variant="table" count={5} />
```

#### Props

- `variant`: "text" | "circle" | "rect" | "card" | "table" (default: "text")
- `width`: number | string (optional)
- `height`: number | string (optional)
- `count`: number (default: 1)
- `animate`: boolean (default: true)
- `className`: string (optional)
- `borderRadius`: string (optional)
- `children`: ReactNode (optional)

### ErrorBanner

The `ErrorBanner` component is used to display error messages, warnings, and empty state messages.

```tsx
import { ErrorBanner } from "@/components/ui/error-banner";

// Error banner
<ErrorBanner 
  title="Error" 
  message="Failed to load data. Please try again later." 
  severity="error" 
/>

// Warning banner
<ErrorBanner 
  title="Warning" 
  message="Some data may be incomplete." 
  severity="warning" 
/>

// Info banner
<ErrorBanner 
  title="Information" 
  message="The system will be undergoing maintenance in 24 hours." 
  severity="info" 
/>

// Empty state banner
<ErrorBanner 
  title="No Results Found" 
  message="There are no items matching your search criteria. Try adjusting your filters." 
  severity="warning" 
/>

// With retry button
<ErrorBanner 
  title="Connection Error" 
  message="Failed to connect to the server." 
  severity="error" 
  onRetry={() => refetch()} 
/>

// Dismissible banner
<ErrorBanner 
  title="Notice" 
  message="This is a dismissible message." 
  severity="info" 
  dismissible 
  onDismiss={() => console.log('Dismissed')} 
/>
```

#### Props

- `title`: string (optional)
- `message`: string
- `severity`: "error" | "warning" | "info" | "success" (default: "error")
- `dismissible`: boolean (default: false)
- `onRetry`: () => void (optional)
- `onDismiss`: () => void (optional)
- `className`: string (optional)
- `children`: ReactNode (optional)

## Usage Guidelines

### When to Use Each Component

- **Spinner**: Use for general loading states when fetching data or performing asynchronous operations.
- **ProgressBar**: Use for operations with measurable progress, such as file uploads or multi-step processes.
- **Skeleton**: Use for content that is loading and has a known structure, such as tables, cards, or text.
- **ErrorBanner**: Use for displaying errors, warnings, empty states, and other messages.

### Loading States

When a component is loading data, use one of the following patterns:

```tsx
// Using Spinner
{isLoading && (
  <div className="text-center p-4">
    <Spinner size="md" color="primary" showText text="Loading..." />
  </div>
)}

// Using Skeleton for tables
{isLoading && (
  <Skeleton variant="table" count={5} />
)}

// Using Skeleton for cards
{isLoading && (
  <Skeleton variant="card" width="100%" height={200} />
)}

// Using ProgressBar for file uploads
{isLoading && (
  <ProgressBar value={progress} color="primary" size="md" showText text={`Uploading... ${progress}%`} />
)}
```

### Empty States

When no data is available, use the ErrorBanner component with a helpful message:

```tsx
{!isLoading && !isError && data.length === 0 && (
  <ErrorBanner
    title="No Results Found"
    message="There are no items matching your search criteria. Try adjusting your filters."
    severity="warning"
  />
)}
```

### Error States

When an error occurs, use the ErrorBanner component with a retry option if applicable:

```tsx
{isError && (
  <ErrorBanner
    title="Error"
    message={error?.message || "An error occurred. Please try again later."}
    severity="error"
    onRetry={() => refetch()}
  />
)}
```

## Accessibility Considerations

- All loading indicators include appropriate ARIA attributes (`role="status"`, `aria-live="polite"`, etc.).
- Progress bars include `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax` attributes.
- Error banners use `role="alert"` for errors and `role="status"` for other severities.
- Screen reader announcements are included for all components.

## Best Practices

1. Always show a loading indicator when fetching data or performing asynchronous operations.
2. Use appropriate loading indicators based on the context and expected duration of the operation.
3. Provide helpful messages in empty states to guide users on what to do next.
4. Include retry options for errors when applicable.
5. Ensure all components are accessible with appropriate ARIA attributes.
6. Use consistent styling and behavior across the application.
7. Consider the user's context and provide appropriate feedback based on the operation being performed.