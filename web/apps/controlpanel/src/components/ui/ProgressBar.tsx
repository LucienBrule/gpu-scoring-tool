"use client";

import React from "react";
import { cn } from "@/lib/utils";

/**
 * Props for the ProgressBar component
 */
export interface ProgressBarProps {
  /**
   * The current progress value (0-100)
   */
  value: number;

  /**
   * The color of the progress bar
   * @default "primary"
   */
  color?: "primary" | "secondary" | "accent" | "success" | "warning" | "danger";

  /**
   * The size/height of the progress bar
   * @default "md"
   */
  size?: "sm" | "md" | "lg";

  /**
   * Whether to show the progress text
   * @default false
   */
  showText?: boolean;

  /**
   * Custom text to display. If not provided, shows "{value}%"
   */
  text?: string;

  /**
   * Additional CSS classes to apply to the container
   */
  className?: string;

  /**
   * Additional CSS classes to apply to the progress bar
   */
  progressClassName?: string;

  /**
   * Additional CSS classes to apply to the text
   */
  textClassName?: string;
}

/**
 * A progress bar component for indicating progress of operations
 */
export function ProgressBar({
  value,
  color = "primary",
  size = "md",
  showText = false,
  text,
  className = "",
  progressClassName = "",
  textClassName = "",
}: ProgressBarProps) {
  // Ensure value is between 0 and 100
  const clampedValue = Math.max(0, Math.min(100, value));
  
  // Determine size classes
  const sizeClasses = {
    sm: "h-1.5",
    md: "h-2.5",
    lg: "h-4",
  };

  // Determine color classes
  const colorClasses = {
    primary: "bg-blue-600 dark:bg-blue-500",
    secondary: "bg-purple-600 dark:bg-purple-500",
    accent: "bg-pink-600 dark:bg-pink-500",
    success: "bg-green-600 dark:bg-green-500",
    warning: "bg-yellow-600 dark:bg-yellow-500",
    danger: "bg-red-600 dark:bg-red-500",
  };

  // Determine text size based on progress bar size
  const textSizeClasses = {
    sm: "text-xs",
    md: "text-sm",
    lg: "text-base",
  };

  return (
    <div className={cn("w-full", className)}>
      {showText && (
        <p 
          className={cn(
            "mb-2 text-gray-500 dark:text-gray-400",
            textSizeClasses[size],
            textClassName
          )}
        >
          {text || `${clampedValue}%`}
        </p>
      )}
      <div 
        className={cn(
          "w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden",
          sizeClasses[size]
        )}
        role="progressbar"
        aria-valuenow={clampedValue}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div 
          className={cn(
            "h-full rounded-full transition-all duration-300 ease-in-out",
            colorClasses[color],
            progressClassName
          )}
          style={{ width: `${clampedValue}%` }}
          data-testid="progress-bar-fill"
        ></div>
      </div>
      <span className="sr-only">{clampedValue}% complete</span>
    </div>
  );
}

export default ProgressBar;