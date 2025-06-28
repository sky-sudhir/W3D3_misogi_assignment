"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function NavBar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Home", path: "/" },
    { name: "Inference Calculator", path: "/inference-calculator" },
  ];

  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center space-x-8">
          <Link href="/" className="text-xl font-bold text-blue-600">
            AI Tools
          </Link>
          <div className="flex space-x-6">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                  pathname === item.path ? "text-blue-600" : "text-gray-600"
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>
        </nav>
      </div>
    </header>
  );
}
