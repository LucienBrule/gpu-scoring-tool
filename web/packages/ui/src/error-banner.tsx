"use client";

import { ReactNode, useState } from "react";
import { X, AlertCircle, AlertTriangle, Info, CheckCircle, RefreshCw } from "lucide-react";

/**
 * Props for the ErrorBanner component
 */
export interface ErrorBannerProps {
  /**
   * The title of the banner
   */
  title?: string;

  /**
   * The message to display
   */
  message: string;

  /**
   * The severity level of the error
   * @default "error"
   */
  severity?: "error" | "warning" | "info" | "success";

  /**
   * Whether the banner can be dismissed
   * @default false
   */
  dismissible?: boolean;

  /**
   * Callback function to retry the operation
   * If provided, a retry button will be shown
   */
  onRetry?: () => void;

  /**
   * Callback function called when the banner is dismissed
   */
  onDismiss?: () => void;

  /**
   * Additional CSS classes to apply
   */
  className?: string;

  /**
   * Additional content to render in the banner
   */
  children?: ReactNode;
}

/**
 * A banner component for displaying errors, warnings, and other messages
 */
export function ErrorBanner({
  title,
  message,
  severity = "error",
  dismissible = false,
  onRetry,
  onDismiss,
  className = "",
  children,
}: ErrorBannerProps) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) {
    return null;
  }

  // Determine the appropriate colors and icon based on severity
  const severityConfig = {
    error: {
      bgColor: "bg-red-100 dark:bg-red-900/20",
      borderColor: "border-red-400 dark:border-red-800",
      textColor: "text-red-700 dark:text-red-300",
      icon: <AlertCircle className="h-5 w-5 text-red-500 dark:text-red-400" aria-hidden="true" />,
      testId: "error-banner-error",
    },
    warning: {
      bgColor: "bg-yellow-100 dark:bg-yellow-900/20",
      borderColor: "border-yellow-400 dark:border-yellow-800",
      textColor: "text-yellow-700 dark:text-yellow-300",
      icon: <AlertTriangle className="h-5 w-5 text-yellow-500 dark:text-yellow-400" aria-hidden="true" />,
      testId: "error-banner-warning",
    },
    info: {
      bgColor: "bg-blue-100 dark:bg-blue-900/20",
      borderColor: "border-blue-400 dark:border-blue-800",
      textColor: "text-blue-700 dark:text-blue-300",
      icon: <Info className="h-5 w-5 text-blue-500 dark:text-blue-400" aria-hidden="true" />,
      testId: "error-banner-info",
    },
    success: {
      bgColor: "bg-green-100 dark:bg-green-900/20",
      borderColor: "border-green-400 dark:border-green-800",
      textColor: "text-green-700 dark:text-green-300",
      icon: <CheckCircle className="h-5 w-5 text-green-500 dark:text-green-400" aria-hidden="true" />,
      testId: "error-banner-success",
    },
  };

  const { bgColor, borderColor, textColor, icon, testId } = severityConfig[severity];

  const handleDismiss = () => {
    setDismissed(true);
    if (onDismiss) {
      onDismiss();
    }
  };

  return (
    <div
      className={`${bgColor} ${borderColor} ${textColor} border px-4 py-3 rounded relative ${className}`}
      role={severity === "error" ? "alert" : "status"}
      aria-live={severity === "error" ? "assertive" : "polite"}
      data-testid={testId}
    >
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-3 mt-0.5">
          {icon}
        </div>
        <div className="flex-1">
          {title && (
            <p className="font-bold mb-1">{title}</p>
          )}
          <p className="text-sm">{message}</p>
          {children && (
            <div className="mt-2">
              {children}
            </div>
          )}
          {onRetry && (
            <button
              onClick={onRetry}
              className={`mt-2 inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md 
                ${severity === "error" ? "bg-red-600 hover:bg-red-700 text-white" : 
                  severity === "warning" ? "bg-yellow-600 hover:bg-yellow-700 text-white" :
                  severity === "info" ? "bg-blue-600 hover:bg-blue-700 text-white" :
                  "bg-green-600 hover:bg-green-700 text-white"}`}
              data-testid="error-banner-retry"
            >
              <RefreshCw className="mr-1.5 h-3 w-3" aria-hidden="true" />
              Retry
            </button>
          )}
        </div>
        {dismissible && (
          <div className="flex-shrink-0 ml-3">
            <button
              type="button"
              className={`${textColor} inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 
                ${severity === "error" ? "focus:ring-red-500" : 
                  severity === "warning" ? "focus:ring-yellow-500" :
                  severity === "info" ? "focus:ring-blue-500" :
                  "focus:ring-green-500"}`}
              onClick={handleDismiss}
              aria-label="Dismiss"
              data-testid="error-banner-dismiss"
            >
              <X className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}