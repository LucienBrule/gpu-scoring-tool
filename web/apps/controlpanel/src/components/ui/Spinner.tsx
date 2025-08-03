"use client";

import React from "react";
import { cn } from "@/lib/utils";

/**
 * Props for the Spinner component
 */
export interface SpinnerProps {
  /**
   * The size of the spinner
   * @default "md"
   */
  size?: "sm" | "md" | "lg";

  /**
   * The color of the spinner
   * @default "primary"
   */
  color?: "primary" | "secondary" | "accent" | "white";

  /**
   * Whether to show a loading text below the spinner
   * @default false
   */
  showText?: boolean;

  /**
   * The text to display below the spinner
   * @default "Loading..."
   */
  text?: string;

  /**
   * Additional CSS classes to apply
   */
  className?: string;

  /**
   * Additional CSS classes to apply to the container
   */
  containerClassName?: string;
}

/**
 * A spinner component for indicating loading states
 */
export function Spinner({
  size = "md",
  color = "primary",
  showText = false,
  text = "Loading...",
  className = "",
  containerClassName = "",
}: SpinnerProps) {
  // Determine size classes
  const sizeClasses = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-b-2",
    lg: "h-12 w-12 border-b-3",
  };

  // Determine color classes
  const colorClasses = {
    primary: "border-primary",
    secondary: "border-secondary",
    accent: "border-accent",
    white: "border-white",
  };

  // Determine text size based on spinner size
  const textSizeClasses = {
    sm: "text-xs",
    md: "text-sm",
    lg: "text-base",
  };

  return (
    <div 
      className={cn(
        "text-center",
        containerClassName
      )}
      role="status"
      aria-live="polite"
    >
      <div 
        className={cn(
          "animate-spin rounded-full mx-auto",
          sizeClasses[size],
          colorClasses[color],
          className
        )}
        aria-hidden="true"
        data-testid="spinner"
      ></div>
      {showText && (
        <p 
          className={cn(
            "mt-2 text-gray-500 dark:text-gray-400",
            textSizeClasses[size]
          )}
        >
          {text}
        </p>
      )}
      <span className="sr-only">{text}</span>
    </div>
  );
}

export default Spinner;