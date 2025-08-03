import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merges class names using clsx and tailwind-merge
 * This utility is used to combine Tailwind CSS classes with conditional logic
 * 
 * @example
 * ```tsx
 * <div className={cn("base-class", condition && "conditional-class", className)}>
 *   Content
 * </div>
 * ```
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}