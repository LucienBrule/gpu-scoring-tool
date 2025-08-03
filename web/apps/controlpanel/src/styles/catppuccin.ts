/**
 * Catppuccin Mocha color palette
 * 
 * This file exports the Catppuccin Mocha color palette as TypeScript constants
 * for use in components and styles. The colors match those defined in tailwind.config.js.
 * 
 * @see https://github.com/catppuccin/catppuccin
 */

// Base colors
export const rosewater = "#f5e0dc";
export const flamingo = "#f2cdcd";
export const pink = "#f5c2e7";
export const mauve = "#cba6f7";
export const red = "#f38ba8";
export const maroon = "#eba0ac";
export const peach = "#fab387";
export const yellow = "#f9e2af";
export const green = "#a6e3a1";
export const teal = "#94e2d5";
export const sky = "#89dceb";
export const sapphire = "#74c7ec";
export const blue = "#89b4fa";
export const lavender = "#b4befe";

// Text and background colors
export const text = "#cdd6f4";
export const subtext1 = "#bac2de";
export const subtext0 = "#a6adc8";
export const overlay2 = "#9399b2";
export const overlay1 = "#7f849c";
export const overlay0 = "#6c7086";
export const surface2 = "#585b70";
export const surface1 = "#45475a";
export const surface0 = "#313244";
export const base = "#1e1e2e";
export const mantle = "#181825";
export const crust = "#11111b";

// Semantic colors
export const primary = mauve; // mauve
export const secondary = blue; // blue
export const accent = pink; // pink
export const warning = yellow; // yellow
export const error = red; // red
export const success = green; // green
export const info = sapphire; // sapphire

// Background and foreground
export const background = base; // base
export const foreground = text; // text

// Export as a complete palette object
export const catppuccinMocha = {
  // Base colors
  rosewater,
  flamingo,
  pink,
  mauve,
  red,
  maroon,
  peach,
  yellow,
  green,
  teal,
  sky,
  sapphire,
  blue,
  lavender,
  
  // Text and background colors
  text,
  subtext1,
  subtext0,
  overlay2,
  overlay1,
  overlay0,
  surface2,
  surface1,
  surface0,
  base,
  mantle,
  crust,

  // Semantic colors
  primary,
  secondary,
  accent,
  warning,
  error,
  success,
  info,
  
  // Background and foreground
  background,
  foreground,
};

export default catppuccinMocha;