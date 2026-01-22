import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

async function proxy(
  request: NextRequest,
  { params }: { params: Promise<{ path?: string[] }> },
  method: string
) {
  const resolvedParams = await params;
  const path = (resolvedParams.path || []).join('/');
  const search = request.nextUrl.search;
  const targetUrl = `${BACKEND_URL}/api/portfolio/${path}${search}`;

  try {
    const hasBody = !['GET', 'HEAD'].includes(method);
    const body = hasBody ? await request.text() : undefined;

    const response = await fetch(targetUrl, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: body && body.length > 0 ? body : undefined,
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Portfolio BFF Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest, ctx: { params: Promise<{ path?: string[] }> }) {
  return proxy(request, ctx, 'GET');
}

export async function POST(
  request: NextRequest,
  ctx: { params: Promise<{ path?: string[] }> }
) {
  return proxy(request, ctx, 'POST');
}

export async function DELETE(
  request: NextRequest,
  ctx: { params: Promise<{ path?: string[] }> }
) {
  return proxy(request, ctx, 'DELETE');
}

export async function PUT(request: NextRequest, ctx: { params: Promise<{ path?: string[] }> }) {
  return proxy(request, ctx, 'PUT');
}

export async function PATCH(
  request: NextRequest,
  ctx: { params: Promise<{ path?: string[] }> }
) {
  return proxy(request, ctx, 'PATCH');
}
