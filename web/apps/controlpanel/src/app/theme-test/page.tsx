'use client';

import ThemeToggle from '@/components/ThemeToggle';
import { catppuccinMocha } from '@/styles/catppuccin';

/**
 * Theme Test Page
 * 
 * This page is used to test the Catppuccin Mocha theme implementation.
 * It displays color swatches for all theme colors and provides a theme toggle.
 */
export default function ThemeTestPage() {
  return (
    <div className="p-8 min-h-screen bg-background text-foreground">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Catppuccin Mocha Theme Test</h1>
        
        <div className="mb-8">
          <ThemeToggle />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {/* Base colors */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Base Colors</h2>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries({
                rosewater: catppuccinMocha.rosewater,
                flamingo: catppuccinMocha.flamingo,
                pink: catppuccinMocha.pink,
                mauve: catppuccinMocha.mauve,
                red: catppuccinMocha.red,
                maroon: catppuccinMocha.maroon,
                peach: catppuccinMocha.peach,
                yellow: catppuccinMocha.yellow,
                green: catppuccinMocha.green,
                teal: catppuccinMocha.teal,
                sky: catppuccinMocha.sky,
                sapphire: catppuccinMocha.sapphire,
                blue: catppuccinMocha.blue,
                lavender: catppuccinMocha.lavender,
              }).map(([name, color]) => (
                <div key={name} className="flex items-center space-x-2">
                  <div 
                    className="w-8 h-8 rounded-md border border-surface1" 
                    style={{ backgroundColor: color }}
                  />
                  <div>
                    <div className="text-sm font-medium">{name}</div>
                    <div className="text-xs opacity-70">{color}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Semantic colors */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Semantic Colors</h2>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries({
                primary: 'bg-primary',
                secondary: 'bg-secondary',
                accent: 'bg-accent',
                warning: 'bg-warning',
                error: 'bg-error',
                success: 'bg-success',
                info: 'bg-info',
              }).map(([name, bgClass]) => (
                <div key={name} className="flex items-center space-x-2">
                  <div className={`w-8 h-8 rounded-md border border-surface1 ${bgClass}`} />
                  <div className="text-sm font-medium">{name}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Surface colors */}
        <div className="space-y-4 mb-12">
          <h2 className="text-xl font-semibold">Surface Colors</h2>
          <div className="flex space-x-4">
            {['bg-surface0', 'bg-surface1', 'bg-surface2', 'bg-base', 'bg-mantle', 'bg-crust'].map((bgClass) => (
              <div key={bgClass} className="text-center">
                <div className={`w-16 h-16 rounded-md border border-surface1 ${bgClass}`} />
                <div className="text-xs mt-1">{bgClass.replace('bg-', '')}</div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Text colors */}
        <div className="space-y-4 mb-12">
          <h2 className="text-xl font-semibold">Text Colors</h2>
          <div className="space-y-2 p-4 bg-surface0 rounded-md">
            <p className="text-text">text-text: Primary text color</p>
            <p className="text-subtext1">text-subtext1: Secondary text color</p>
            <p className="text-subtext0">text-subtext0: Tertiary text color</p>
            <p className="text-overlay2">text-overlay2: Subtle text color</p>
            <p className="text-overlay1">text-overlay1: Very subtle text color</p>
            <p className="text-overlay0">text-overlay0: Extremely subtle text color</p>
          </div>
        </div>
        
        {/* UI Components */}
        <div className="space-y-4 mb-12">
          <h2 className="text-xl font-semibold">UI Components</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-surface0 rounded-md">
              <h3 className="font-medium mb-2">Buttons</h3>
              <div className="flex flex-wrap gap-2">
                <button className="px-4 py-2 bg-primary text-base rounded-md">Primary</button>
                <button className="px-4 py-2 bg-secondary text-base rounded-md">Secondary</button>
                <button className="px-4 py-2 bg-accent text-base rounded-md">Accent</button>
                <button className="px-4 py-2 bg-surface1 text-text rounded-md">Default</button>
              </div>
            </div>
            
            <div className="p-4 bg-surface0 rounded-md">
              <h3 className="font-medium mb-2">Alerts</h3>
              <div className="space-y-2">
                <div className="p-2 bg-info/20 border-l-4 border-info rounded-md">Info message</div>
                <div className="p-2 bg-success/20 border-l-4 border-success rounded-md">Success message</div>
                <div className="p-2 bg-warning/20 border-l-4 border-warning rounded-md">Warning message</div>
                <div className="p-2 bg-error/20 border-l-4 border-error rounded-md">Error message</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}