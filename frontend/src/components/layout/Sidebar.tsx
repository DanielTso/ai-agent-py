"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { clsx } from "clsx";
import {
  LayoutDashboard,
  AlertTriangle,
  CalendarClock,
  FileText,
  ShieldCheck,
  Truck,
  DollarSign,
  HardHat,
  Wrench,
  Leaf,
  Scale,
  MapPin,
  HeartPulse,
  CheckCircle2,
  Bot,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/risks", label: "Risks", icon: AlertTriangle },
  { href: "/schedule", label: "Schedule", icon: CalendarClock },
  { href: "/documents", label: "Documents", icon: FileText },
  { href: "/compliance", label: "Compliance", icon: ShieldCheck },
  { href: "/supply-chain", label: "Supply Chain", icon: Truck },
  { href: "/financial", label: "Financial", icon: DollarSign },
  { href: "/workforce", label: "Workforce", icon: HardHat },
  { href: "/commissioning", label: "Commissioning", icon: Wrench },
  { href: "/environmental", label: "Environmental", icon: Leaf },
  { href: "/claims", label: "Claims", icon: Scale },
  { href: "/site-logistics", label: "Site Logistics", icon: MapPin },
  { href: "/safety", label: "Safety", icon: HeartPulse },
  { href: "/approvals", label: "Approvals", icon: CheckCircle2 },
  { href: "/agents", label: "Agents", icon: Bot },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={clsx(
        "fixed left-0 top-0 h-screen bg-white border-r border-gray-200 flex flex-col transition-all z-30",
        collapsed ? "w-16" : "w-[var(--sidebar-width)]",
      )}
    >
      <div className="flex items-center justify-between px-4 h-14 border-b border-gray-200">
        {!collapsed && (
          <span className="font-bold text-primary text-sm truncate">
            Construction PM
          </span>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 rounded hover:bg-gray-100"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto py-2">
        {NAV_ITEMS.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 px-4 py-2.5 text-sm transition-colors",
                isActive
                  ? "bg-primary/10 text-primary font-medium border-r-2 border-primary"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900",
              )}
              title={collapsed ? item.label : undefined}
            >
              <Icon size={18} className="flex-shrink-0" />
              {!collapsed && <span className="truncate">{item.label}</span>}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
