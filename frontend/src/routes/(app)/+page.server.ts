import client from '$lib/clients/v1/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
  const { data: posts_data } = await client.GET('/api/v1/posts/');

  return { posts: posts_data };
};
