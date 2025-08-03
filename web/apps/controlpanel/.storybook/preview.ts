import type { Preview, Decorator } from '@storybook/react-vite';
import '../src/app/globals.css';

// Dark mode decorator
const withDarkMode: Decorator = (StoryFn, context) => {
  const { theme } = context.globals;
  
  // Add dark class to html element for dark mode
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  
  // Create a wrapper div with appropriate classes
  const wrapper = document.createElement('div');
  wrapper.className = `${theme === 'dark' ? 'dark' : ''} min-h-screen bg-white dark:bg-gray-900 p-6`;
  
  // Render the story into the wrapper
  const story = StoryFn();
  
  // Return the story with the wrapper applied
  return {
    ...story,
    render: () => {
      const originalRender = story.render || (() => story.template);
      return originalRender();
    }
  };
};

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a202c' },
      ],
    },
  },
  decorators: [withDarkMode],
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        icon: 'circlehollow',
        items: [
          { value: 'light', icon: 'sun', title: 'Light' },
          { value: 'dark', icon: 'moon', title: 'Dark' },
        ],
        showName: true,
      },
    },
  },
};

export default preview;