const LoadingPage = () => {
  return (
    <main className="min-h-screen flex items-center justify-center bg-[#F5F5F5] relative">
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: 'radial-gradient(circle, rgba(0,0,0,0.12) 1px, transparent 1px)',
          backgroundSize: '18px 18px',
        }}
      />
      <div className="relative z-10 w-10 h-10 border-3 border-[#A15EED]/30 border-t-[#A15EED] rounded-full animate-spin" />
    </main>
  );
};

export default LoadingPage;
