import React from 'react';
import { createRoot } from 'react-dom/client';
import MemberDashboard from './MemberDashboard';
import '../../css/input.css';

const root = document.getElementById('root');
if (root) {
  createRoot(root).render(<MemberDashboard />);
}
