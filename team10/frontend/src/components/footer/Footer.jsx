import React from "react";
import { Facebook, Twitter, Instagram } from "lucide-react";

export default function Footer() {
  return (
    <>
      <hr className="border-gray-300 mt-12" />
      <div className="bg-gray-800 text-white py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm">
            <p>© Rakuten Group, Inc.</p>
          </div>
        </div>
      </div>
    </>
  );
}
