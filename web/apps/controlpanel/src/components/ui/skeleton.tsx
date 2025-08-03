"use client";

import React, { ReactNode } from "react";

/**
 * Props for the Skeleton component
 */
export interface SkeletonProps {
  /**
   * The variant of the skeleton
   * - text: A line of text (default)
   * - circle: A circular skeleton
   * - rect: A rectangular skeleton
   * - card: A card-like skeleton
   * - table: A table row skeleton
   */
  variant?: "text" | "circle" | "rect" | "card" | "table";

  /**
   * The width of the skeleton
   * Can be a number (px) or a string (e.g., "100%", "12rem")
   */
  width?: number | string;

  /**
   * The height of the skeleton
   * Can be a number (px) or a string (e.g., "100%", "3rem")
   */
  height?: number | string;

  /**
   * The number of items to render (for text and table variants)
   */
  count?: number;

  /**
   * Whether to show the animation
   * @default true
   */
  animate?: boolean;

  /**
   * Additional CSS classes to apply
   */
  className?: string;

  /**
   * The border radius of the skeleton
   * @default "0.25rem" (4px)
   */
  borderRadius?: string;

  /**
   * Children to render inside the skeleton (for custom layouts)
   */
  children?: ReactNode;
}

/**
 * A skeleton loading component that can be used to indicate content is loading
 */
export function Skeleton({
  variant = "text",
  width,
  height,
  count = 1,
  animate = true,
  className = "",
  borderRadius,
  children,
}: SkeletonProps) {
  // Base classes for all skeleton variants
  const baseClasses = `
    bg-gray-200 dark:bg-gray-700
    ${animate ? "animate-pulse" : ""}
  `;

  // Determine width and height styles
  const widthStyle = width !== undefined
    ? typeof width === "number" ? `${width}px` : width
    : variant === "text" ? "100%" : undefined;
  
  const heightStyle = height !== undefined
    ? typeof height === "number" ? `${height}px` : height
    : getDefaultHeight(variant);

  // Determine border radius
  const radiusStyle = borderRadius || getDefaultRadius(variant);

  // Generate the appropriate skeleton based on variant
  const renderSkeleton = () => {
    switch (variant) {
      case "circle":
        return (
          <div
            className={`${baseClasses} rounded-full ${className}`}
            style={{
              width: widthStyle || heightStyle,
              height: heightStyle,
              borderRadius: "50%",
            }}
            aria-hidden="true"
            data-testid="skeleton-circle"
          >
            {children}
          </div>
        );
      
      case "card":
        return (
          <div
            className={`${baseClasses} ${className}`}
            style={{
              width: widthStyle || "100%",
              height: heightStyle,
              borderRadius: radiusStyle,
            }}
            aria-hidden="true"
            data-testid="skeleton-card"
          >
            {children || (
              <div className="p-4">
                <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-1/2 mb-2"></div>
                <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-2/3"></div>
              </div>
            )}
          </div>
        );
      
      case "table":
        return (
          <div
            className={`w-full ${className}`}
            aria-hidden="true"
            data-testid="skeleton-table"
          >
            {Array.from({ length: count }).map((_, index) => (
              <div
                key={index}
                className={`${baseClasses} flex items-center h-12 mb-2 rounded`}
                style={{ borderRadius: radiusStyle }}
              >
                {Array.from({ length: 5 }).map((_, cellIndex) => (
                  <div
                    key={cellIndex}
                    className="h-4 bg-gray-300 dark:bg-gray-600 rounded mx-4"
                    style={{ width: `${Math.floor(0.15 * 30) + 10}%` }}
                  ></div>
                ))}
              </div>
            ))}
          </div>
        );
      
      case "rect":
        return (
          <div
            className={`${baseClasses} ${className}`}
            style={{
              width: widthStyle || "100%",
              height: heightStyle,
              borderRadius: radiusStyle,
            }}
            aria-hidden="true"
            data-testid="skeleton-rect"
          >
            {children}
          </div>
        );
      
      case "text":
      default:
        return (
          <div
            className={`w-full ${className}`}
            aria-hidden="true"
            data-testid="skeleton-text"
          >
            {Array.from({ length: count }).map((_, index) => (
              <div
                key={index}
                className={`${baseClasses} h-4 mb-2 rounded`}
                style={{
                  width: index === count - 1 ? "80%" : "100%",
                  borderRadius: radiusStyle,
                }}
              ></div>
            ))}
          </div>
        );
    }
  };

  return renderSkeleton();
}

// Helper functions to get default heights and border radius based on variant
function getDefaultHeight(variant: SkeletonProps["variant"]): string {
  switch (variant) {
    case "text":
      return "1rem";
    case "circle":
      return "3rem";
    case "rect":
      return "6rem";
    case "card":
      return "12rem";
    case "table":
      return "auto";
    default:
      return "1rem";
  }
}

function getDefaultRadius(variant: SkeletonProps["variant"]): string {
  switch (variant) {
    case "text":
      return "0.25rem";
    case "circle":
      return "50%";
    case "rect":
      return "0.25rem";
    case "card":
      return "0.5rem";
    case "table":
      return "0.25rem";
    default:
      return "0.25rem";
  }
}