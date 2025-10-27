"use client";
import React from "react";

export default function Footer() {
  return (
    <footer style={{
      background:"#1e1e1e", color:"#fff", textAlign:"center", padding:"12px 16px", marginTop:24
    }}>
      © {new Date().getFullYear()} Movie Munchers
    </footer>
  );
}
