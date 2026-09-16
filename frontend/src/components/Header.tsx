'use client';

import React from 'react';

interface HeaderProps {
  theme: 'light' | 'dark';
  onToggleTheme: () => void;
  onOpenDemoModal: () => void;
}

export default function Header({
  theme,
  onToggleTheme,
  onOpenDemoModal,
}: HeaderProps) {
  return (
    <header className="h-14 px-4 sm:px-6 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-between z-20 transition-colors">
      <div className="flex items-center gap-2.5">
        <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white shadow-sm font-bold text-sm">
          ⚡
        </div>
        <div>
          <div className="flex items-baseline gap-2">
            <h1 className="font-bold text-base tracking-tight text-slate-900 dark:text-slate-100 leading-none">
              VoltRoute
            </h1>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-normal leading-none hidden sm:inline">
              EV route planning
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {/* Popular Routes */}
        <button
          type="button"
          onClick={onOpenDemoModal}
          className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
        >
          <span>🛣️</span>
          <span>Popular Routes</span>
        </button>

        {/* Dark/Light Theme Toggle */}
        <button
          type="button"
          onClick={onToggleTheme}
          aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          className="w-8 h-8 flex items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-sm"
        >
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
      </div>
    </header>
  );
}

