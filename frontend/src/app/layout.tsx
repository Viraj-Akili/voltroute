import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VoltRoute — Intelligent EV Route Planner",
  description: "Advanced EV route planning web application that simulates battery consumption and optimizes fast-charging stops to minimize total trip time.",
  keywords: ["EV", "Electric Vehicle", "Route Planner", "Tesla Supercharger", "Electrify America", "EV Charging", "Fast Charging", "Navigation"],
  authors: [{ name: "VoltRoute Team" }],
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>" />
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
      </head>
      <body className="bg-space-900 text-slate-100 antialiased min-h-screen flex flex-col selection:bg-volt-500 selection:text-space-900">
        {children}
      </body>
    </html>
  );
}
