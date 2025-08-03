"use client";

import React, { forwardRef } from "react";

// Button variants
type ButtonVariant = "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";

// Button sizes
type ButtonSize = "default" | "sm" | "lg" | "icon";

// Button component props
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  asChild?: boolean;
  className?: string;
}

// Button component
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    className = "", 
    variant = "default", 
    size = "default", 
    asChild = false,
    type = "button",
    ...props 
  }, ref) => {
    // Determine variant-specific styles
    const variantStyles = {
      default: "bg-primary text-primary-foreground hover:bg-primary/90 dark:bg-primary dark:text-primary-foreground dark:hover:bg-primary/90",
      destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90 dark:bg-red-600 dark:text-white dark:hover:bg-red-700",
      outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground dark:border-gray-600 dark:bg-transparent dark:hover:bg-gray-800",
      secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600",
      ghost: "hover:bg-accent hover:text-accent-foreground dark:hover:bg-gray-800 dark:hover:text-gray-200",
      link: "text-primary underline-offset-4 hover:underline dark:text-blue-400 dark:hover:text-blue-300",
    };

    // Determine size-specific styles
    const sizeStyles = {
      default: "h-10 px-4 py-2",
      sm: "h-9 rounded-md px-3",
      lg: "h-11 rounded-md px-8",
      icon: "h-10 w-10",
    };

    return (
      <button
        type={type}
        className={`inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
        ref={ref}
        {...props}
      />
    );
  }
);

// Set display name for debugging
Button.displayName = "Button";
