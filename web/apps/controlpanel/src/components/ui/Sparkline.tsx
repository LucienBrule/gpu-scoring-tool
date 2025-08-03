"use client";

import React, { useMemo } from "react";
import { cn } from "@/lib/utils";

/**
 * Props for the Sparkline component
 */
export interface SparklineProps {
  /**
   * Array of numeric values to plot
   */
  data: number[];

  /**
   * Width of the sparkline in pixels
   * @default 100
   */
  width?: number;

  /**
   * Height of the sparkline in pixels
   * @default 24
   */
  height?: number;

  /**
   * Color of the sparkline
   * @default "currentColor"
   */
  color?: string;

  /**
   * Width of the stroke in pixels
   * @default 2
   */
  strokeWidth?: number;

  /**
   * Whether to fill the area under the curve
   * @default false
   */
  gradientFill?: boolean;

  /**
   * Additional CSS classes to apply to the SVG
   */
  className?: string;
}

/**
 * A lightweight sparkline component for visualizing trends
 */
export function Sparkline({
  data,
  width = 100,
  height = 24,
  color = "currentColor",
  strokeWidth = 2,
  gradientFill = false,
  className = "",
}: SparklineProps) {
  // Generate a unique ID for the gradient
  const gradientId = useMemo(() => `sparkline-gradient-${Math.random().toString(36).substring(2, 9)}`, []);

  // Generate the path for the sparkline
  const path = useMemo(() => {
    // Handle empty or single-value data arrays
    if (!data || data.length === 0) {
      // Render a flat line at mid-height
      return `M0,${height / 2} L${width},${height / 2}`;
    }

    if (data.length === 1) {
      // Render a flat line at mid-height
      return `M0,${height / 2} L${width},${height / 2}`;
    }

    // Find min and max values for scaling
    const min = Math.min(...data);
    const max = Math.max(...data);
    
    // If min and max are the same, render a flat line
    if (min === max) {
      const y = height / 2;
      return `M0,${y} L${width},${y}`;
    }

    // Calculate the scaling factors
    const xScale = width / (data.length - 1);
    const yScale = height / (max - min);

    // Generate the path
    return data.map((value, index) => {
      const x = index * xScale;
      // Invert y-axis (SVG 0,0 is top-left)
      const y = height - ((value - min) * yScale);
      return `${index === 0 ? 'M' : 'L'}${x},${y}`;
    }).join(' ');
  }, [data, width, height]);

  // Generate the fill path for the area under the curve
  const fillPath = useMemo(() => {
    if (!data || data.length <= 1) {
      return '';
    }

    // Find min and max values for scaling
    const min = Math.min(...data);
    const max = Math.max(...data);
    
    // If min and max are the same, don't render a fill
    if (min === max) {
      return '';
    }

    // Calculate the scaling factors
    const xScale = width / (data.length - 1);
    const yScale = height / (max - min);

    // Generate the path with a closed area to the bottom
    let fillPath = data.map((value, index) => {
      const x = index * xScale;
      // Invert y-axis (SVG 0,0 is top-left)
      const y = height - ((value - min) * yScale);
      return `${index === 0 ? 'M' : 'L'}${x},${y}`;
    }).join(' ');

    // Close the path to form a filled area
    fillPath += ` L${width},${height} L0,${height} Z`;
    
    return fillPath;
  }, [data, width, height]);

  // Generate a descriptive label for screen readers
  const ariaLabel = useMemo(() => {
    if (!data || data.length === 0) {
      return "Empty sparkline";
    }
    
    const min = Math.min(...data);
    const max = Math.max(...data);
    const trend = data[0] < data[data.length - 1] ? "upward" : data[0] > data[data.length - 1] ? "downward" : "flat";
    
    return `Sparkline with ${data.length} points, showing ${trend} trend from ${min} to ${max}`;
  }, [data]);

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className={cn("overflow-visible", className)}
      role="img"
      aria-label={ariaLabel}
    >
      {gradientFill && (
        <defs>
          <linearGradient
            id={gradientId}
            x1="0%"
            y1="0%"
            x2="0%"
            y2="100%"
          >
            <stop
              offset="0%"
              stopColor={color}
              stopOpacity="0.3"
            />
            <stop
              offset="100%"
              stopColor={color}
              stopOpacity="0.05"
            />
          </linearGradient>
        </defs>
      )}
      
      {gradientFill && fillPath && (
        <path
          d={fillPath}
          fill={`url(#${gradientId})`}
          data-testid="sparkline-fill"
        />
      )}
      
      <path
        d={path}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        data-testid="sparkline-path"
      />
    </svg>
  );
}

export default Sparkline;