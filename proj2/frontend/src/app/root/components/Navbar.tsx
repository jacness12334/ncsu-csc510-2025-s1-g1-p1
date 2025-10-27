"use client";
import React from "react";

export default function Navbar() {
  return (
    <nav style={{
      background:"#1e1e1e", color:"#fff", padding:"12px 16px",
      display:"flex", justifyContent:"space-between", alignItems:"center"
    }}>
      <strong>🎬 Movie Munchers</strong>
      <div style={{display:"flex", gap:"12px"}}>
        <a href="#" style={{color:"#fff"}}>Home</a>
        <a href="#" style={{color:"#fff"}}>Menu</a>
        <a href="#" style={{color:"#fff"}}>Orders</a>
      </div>
    </nav>
  );
}
