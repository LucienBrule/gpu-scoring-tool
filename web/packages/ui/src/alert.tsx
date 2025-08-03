"use client";

import React from "react";

// Alert component variants
type AlertVariant = "default" | "destructive" | "success" | "warning" | "info";

// Alert component props
interface AlertProps {
  variant?: AlertVariant;
  className?: string;
  children: React.ReactNode;
}

// Alert component
export function Alert({
  variant = "default",
  className = "",
  children,
}: AlertProps) {
  // Determine variant-specific styles
  const variantStyles = {
    default: "bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-800 dark:text-gray-100 dark:border-gray-700",
    destructive: "bg-red-50 text-red-800 border-red-200 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800",
    success: "bg-green-50 text-green-800 border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800",
    warning: "bg-yellow-50 text-yellow-800 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-300 dark:border-yellow-800",
    info: "bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800",
  };

  return (
    <div
      role="alert"
      className={`relative w-full rounded-lg border p-4 ${variantStyles[variant]} ${className}`}
    >
      {children}
    </div>
  );
}

// AlertTitle component props
interface AlertTitleProps {
  className?: string;
  children: React.ReactNode;
}

// AlertTitle component
export function AlertTitle({ className = "", children }: AlertTitleProps) {
  return (
    <h5 className={`mb-1 font-medium leading-none tracking-tight ${className}`}>
      {children}
    </h5>
  );
}

// AlertDescription component props
interface AlertDescriptionProps {
  className?: string;
  children: React.ReactNode;
}

// AlertDescription component
export function AlertDescription({
  className = "",
  children,
}: AlertDescriptionProps) {
  return (
    <div className={`text-sm ${className}`}>
      {children}
    </div>
  );
}