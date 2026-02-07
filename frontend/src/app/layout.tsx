import type { Metadata } from "next";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { AlertBanner } from "@/components/layout/AlertBanner";
import "./globals.css";

export const metadata: Metadata = {
  title: "Construction PM - AI Dashboard",
  description: "AI-powered construction project management dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Sidebar />
        <div className="ml-[var(--sidebar-width)] min-h-screen flex flex-col">
          <AlertBanner
            message="Steel delivery delay detected - 3 vendors affected. Review supply chain alerts."
            severity="warning"
          />
          <Header />
          <main className="flex-1 p-6">{children}</main>
        </div>
      </body>
    </html>
  );
}
