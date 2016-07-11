import { Injectable } from 'angular2/core';
import { AuthHttp } from '../../shared/auth-request.service';

import {Http, Response, RequestOptions, Headers, Request, RequestMethod} from 'angular2/http';


import { Hero } from './hero.model';
import { HEROES } from '../mock-heroes';

@Injectable()
export class HeroService {
  constructor(
    private http: AuthHttp) {
  }

  getHeroes() {
    return Promise.resolve(HEROES);
  }

  getHeroesSlowly() {
    return new Promise<Hero[]>(resolve =>
      setTimeout(()=>resolve(HEROES), 2000) // 2 seconds
    );
  }

  getHero(id: number) {
    return Promise.resolve(HEROES).then(
      heroes => heroes.filter(hero => hero.id === id)[0]
    );
  }
}
