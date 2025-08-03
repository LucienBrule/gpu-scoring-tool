"use client";

import React, { forwardRef } from "react";

// Label component props
interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  className?: string;
}

// Label component
export const Label = forwardRef<HTMLLabelElement, LabelProps>(
  ({ className = "", ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={`text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 dark:text-gray-300 ${className}`}
        {...props}
      />
    );
  }
);

// Set display name for debugging
Label.displayName = "Label";