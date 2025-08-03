"use client";

import React, { forwardRef } from "react";

// Checkbox component props
interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  checked?: boolean;
  defaultChecked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  required?: boolean;
  name?: string;
  value?: string;
  id?: string;
  className?: string;
}

// Checkbox component
export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  (
    {
      checked,
      defaultChecked,
      onCheckedChange,
      disabled = false,
      required = false,
      name,
      value,
      id,
      className = "",
      ...props
    },
    ref
  ) => {
    // Handle change event
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      onCheckedChange?.(event.target.checked);
    };

    return (
      <div className="relative flex items-center">
        <input
          type="checkbox"
          ref={ref}
          id={id}
          name={name}
          value={value}
          checked={checked}
          defaultChecked={defaultChecked}
          onChange={handleChange}
          disabled={disabled}
          required={required}
          className={`
            h-4 w-4 rounded border border-gray-300 text-primary 
            focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2
            disabled:cursor-not-allowed disabled:opacity-50
            dark:border-gray-600 dark:bg-gray-800 dark:ring-offset-gray-900
            dark:checked:bg-primary dark:focus:ring-primary
            ${className}
          `}
          {...props}
        />
      </div>
    );
  }
);

// Set display name for debugging
Checkbox.displayName = "Checkbox";